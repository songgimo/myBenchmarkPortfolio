import inspect
import re
import time
import random
import queue

from multiprocessing import Process

from PyQt5.QtCore import QObject

from modules.kiwoom.settings import *
from modules.global_settings import REDIS_SERVER, RedisKeys
from modules.utils import set_redis, get_redis


def generate_redis_key(*args):
    return '_'.join(args)


class DynamicApis(object):
    def __init__(self, controller):
        self._dynamic_call = controller.dynamicCall

    def set_value(self, name, value):
        return self._dynamic_call('SetInputValue(QString, QString)', name, value)

    def request_common_data(self, request_name, tx_code, screen_number, repeat):
        return self._dynamic_call('commRqData(QString, QString, int, QString)',
                                  [request_name, tx_code, repeat, screen_number])

    def request_common_kiwoom_data(self, code_list, repeat, code_list_length, n_type, request_name, screen_number):
        return self._dynamic_call('CommKwRqData(QString, int, int, int, QString, QString)',
                                  [code_list, repeat, code_list_length, n_type, request_name, screen_number])

    def send_order(self, request_name, screen_number, account, order_type, stock_code, quantity,
                   price, trade_type, origin_order_number):
        return self._dynamic_call('SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)',
                                  [request_name, screen_number, account, order_type, stock_code,
                                   quantity, price, trade_type, origin_order_number])

    def get_common_data(self, tx_code, rc_name, index, item_name):
        return self._dynamic_call('GetCommData(QString, QString, int, QString)',
                                  [tx_code, rc_name, index, item_name]).replace(' ', '')

    def get_common_data_with_repeat(self, tx_code, request_name, index, item_name):
        return self._dynamic_call('GetCommData(QString, QString, int, QString)',
                                  [tx_code, request_name, index, item_name]).replace(' ', '')

    def get_code_list_by_markets(self, code_list):
        return self._dynamic_call("GetCodeListByMarket(QString)", code_list).split(';')

    def get_repeat_count(self, tx_code, request_name):
        return self._dynamic_call('GetRepeatCnt(QString, QString)', [tx_code, request_name])


class KiwoomAPIModule(QObject, Process):
    def __init__(self, controller):
        super(KiwoomAPIModule, self).__init__()

        self._controller = controller
        self._apis = DynamicApis(controller)

        self._local_queue = queue.Queue()
        self._receiver = Receiver(self._apis, self._local_queue)

    def run(self):
        while True:
            try:
                result = get_redis(RedisKeys.Kiwoom.API_KEY)
            except:
                # redis timeout
                continue

            fn = getattr(self, result['command'])

            result = fn(**result['kwargs'])

            set_redis(RedisKeys.Kiwoom.COM_TO_MODULE_RESULT_KEY, result)

    def connect_all_block(self):
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name.startswith('connect_block'):
                fn()

    def connect_all_real(self):
        for name, fn in inspect.getmembers(self, inspect.ismethod):
            if name.startswith('connect_real'):
                fn()

    def get_all_korean_stock_code(self):
        return {
            "kospi": self.get_kospi_code_list(),
            "kosdaq": self.get_kosdaq_code_list()
        }

    def get_all_korean_name(self, code_list):
        length_ = len(code_list)
        string_code_list = ';'.join(code_list)
        key = generate_redis_key(ItemName.BULK_STOCK_NAME, string_code_list)

        self._apis.request_common_kiwoom_data(
            string_code_list,
            IsRepeat.NO,
            length_,
            NTypes.INTEREST_STOCK_INFO,
            key,
            CustomScreenNumbers.GET_ALL_STOCK_KOREAN_NAME
        )

        return get_redis(key)

    def connect_block_tx_data(self):
        self.OnReceiveTrData.connect(self._receiver.blocking.get_tx_data)

    def connect_block_chejan_data(self):
        self.OnReceiveChejanData.connect(self._receiver.real.get_tx_data)

    def connect_block_message_data(self):
        self.OnReceiveMsg.connect(self._receiver.blocking.get_message)

    def get_stock_code_information(self, stock_code, item_name):
        self._apis.set_value(ValueName.STOCK_CODE, stock_code)

        key = generate_redis_key(item_name)

        self._apis.request_common_data(key, OptCodes.STOCK_INFO, stock_code, IsRepeat.NO)

        raw_data = get_redis(key)

        return re.sub(r'[^\d]', '', raw_data) if raw_data.is_numeric() else raw_data

    def get_all_daily_candle(self, stock_code, date, repeat):
        request_name = generate_redis_key(stock_code, ItemName.DAILY_STOCK_PRICE)
        self._apis.set_value(ValueName.STOCK_CODE, stock_code)
        self._apis.set_value(ValueName.BASE_DATE, date)
        self._apis.set_value(ValueName.FIXED_STOCK_PRICE, 1)

        if self.set_auto_screen:
            self._auto_screen_setter()

        self._apis.request_common_data(request_name, OptCodes.DAILY_CHART, self._auto_screen_number, repeat)

    def get_stock_korean_name(self, stock_code):
        return self.get_stock_code_information(stock_code, ItemName.STOCK_NAME)

    def get_stock_highest_price(self, stock_code):
        return self.get_stock_code_information(stock_code, ItemName.UPPER_LIMIT_PRICE)

    def get_stock_opening_price(self, stock_code):
        return self.get_stock_code_information(stock_code, ItemName.OPENING_PRICE)

    def get_stock_current_price(self, stock_code):
        return self.get_stock_code_information(stock_code, ItemName.CURRENT_PRICE)

    def get_kospi_code_list(self):
        return self._apis.get_code_list_by_markets(StockCodes.KOSPI)

    def get_kosdaq_code_list(self):
        return self._apis.get_code_list_by_markets(StockCodes.KOSDAQ)

    def get_all_daily_thread(self, code, latest_date, input_date, is_repeat):
        def get_stocks_daily_candle_not_entered(ds, date):
            for n, data in enumerate(ds):
                if date in data:
                    # 오늘 제외, 전날부터 미입력 값 넣어야 함.
                    # 최대 600일전까지 나오는데, 그정도로 값이 갱신이 안되진 않을 것이라고 판단함.
                    return ds[:n]

        total_data_set = list()
        while True:
            self.get_all_daily_candle(code, latest_date.strftime('%Y%m%d'), is_repeat)
            is_repeat, data_set = get_redis()
            if input_date:
                # 기존 데이터가 있는 경우, 1회 데이터 추가
                not_entered = get_stocks_daily_candle_not_entered(data_set, input_date[0][0])
                if not_entered:
                    total_data_set += not_entered
                break
            else:
                # 반복시 마지막 날짜를 기준으로 가져오므로
                if is_repeat is False:
                    # 반복상태가 아닌 경우 break해서 수집종료
                    total_data_set += data_set
                    break
                else:
                    total_data_set += data_set[:-1]
                time.sleep(random.randrange(200, 4000) / 1000)

        set_redis()


class Receiver(object):
    def __init__(self, apis, local_queue):
        self.apis = apis
        self.local_queue = local_queue
        self.blocking = self.Blocking(self)
        self.real = self.RealTime(self)

    class Blocking:
        def __init__(self, parent):
            self._apis = parent.apis
            self._local_queue = parent.local_queue

        def get_data_by_request_name(self, request_name):
            if '_' not in request_name:
                return {
                    "item_name": request_name,
                    "parameter": None
                }
            else:
                split = request_name.split('_')
                request_name, parameter = split[0], split[1:]
                return {
                    "item_name": request_name,
                    "parameter": parameter
                }

        def get_tx_data(self, *args):
            screen_number, request_name, tx_code, rc_name, repeat, d_len, error_code, message, sp_message = args

            item_name, parameter = self.get_data_by_request_name(request_name)
            if not parameter:
                result = self._apis.get_common_data(tx_code, rc_name, repeat, item_name)
            else:
                repeat_count = self._apis.get_repeat_count(tx_code, request_name)
                total = dict()
                if item_name == ItemName.BULK_STOCK_NAME:
                    items = (('code', ItemName.STOCK_NAME),)

                elif item_name == ItemName.CURRENT_ACCOUNT_INFO:
                    items = (('code', ItemName.STOCK_CODE), ('current_stock', ItemName.CURRENT_AMOUNT))

                elif item_name == ItemName.STOCKS_HMWD:
                    pass

                elif item_name == ItemName.DAILY_STOCK_PRICE:
                    for i in range(repeat_count):
                        items = (
                             ('date', ItemName.DATE),
                             ('close', ItemName.CURRENT_PRICE),
                             ('open', ItemName.OPENING_PRICE),
                             ('high', ItemName.HIGHEST_PRICE),
                             ('low', ItemName.LOWEST_PRICE),
                         )
                        date_timestamp = datetime.datetime.strptime(date, '%Y%m%d').timestamp() * 1000
                        data_set.append([date_timestamp, open_, high, low, close])
                    else:
                        self._service_q[rq_name].put((False, data_set))

                    self._local_queue.put()

                for each in range(repeat_count):
                    for key, item_name in items:
                        total[key] = self._apis.get_common_data_with_repeat(tx_code, request_name, item_name)
            result = {
                "repeat": int(repeat),
                "total": total
            }
            key = generate_redis_key(tx_code, request_name)

            set_redis(key, result)

        def get_chejan_data(self):
            pass

        def get_message(self):
            pass

    class RealTime:
        def __init__(self, parent):
            self._apis = parent.apis

        def get_tx_data(self):
            pass

        def get_condition(self):
            pass
