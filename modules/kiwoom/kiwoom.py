import inspect
import re
from multiprocessing import Process

from PyQt5.QtCore import QObject

from modules.kiwoom.settings import *
from modules.global_settings import REDIS_SERVER, RedisKeys


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

        self._receiver = Receiver(self._apis)

    def run(self):
        while True:
            try:
                command = REDIS_SERVER.get(RedisKeys.KIWOOM_API_KEY)
            except:
                # redis timeout
                continue

            fn = getattr(self, command)

            result = fn()

            REDIS_SERVER.set(RedisKeys.COM_TO_MODULE_RESULT_KEY, result)

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

        return REDIS_SERVER.get(key)

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

        raw_data = REDIS_SERVER.get(key)

        return re.sub(r'[^\d]', '', raw_data) if raw_data.is_numeric() else raw_data

    def get_stock_korean_name(self, stock_code):
        return self.get_stock_code_information(stock_code, ItemName.STOCK_NAME)

    def get_stock_highest_price(self, stock_code):
        return self.get_stock_code_information(stock_code, ItemName.HIGHEST_PRICE)

    def get_stock_opening_price(self, stock_code):
        return self.get_stock_code_information(stock_code, ItemName.OPENING_PRICE)

    def get_stock_current_price(self, stock_code):
        return self.get_stock_code_information(stock_code, ItemName.CURRENT_PRICE)

    def get_kospi_code_list(self):
        return self._apis.get_code_list_by_markets(StockCodes.KOSPI)

    def get_kosdaq_code_list(self):
        return self._apis.get_code_list_by_markets(StockCodes.KOSDAQ)


class Receiver(object):
    def __init__(self, apis):
        self.apis = apis
        self.blocking = self.Blocking(self)
        self.real = self.RealTime(self)

    class Blocking:
        def __init__(self, parent):
            self._apis = parent.apis

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

            if parameter:
                repeat_count = self._apis.get_repeat_count(tx_code, request_name)
                total = dict()
                if item_name == ItemName.BULK_STOCK_NAME:
                    items = (('code', ItemName.STOCK_NAME),)

                elif item_name == ItemName.CURRENT_ACCOUNT_INFO:
                    items = (('code', ItemName.STOCK_CODE), ('current_stock', ItemName.CURRENT_AMOUNT))

                elif item_name == ItemName.STOCKS_HMWD:
                    pass

                for each in repeat_count:
                    for key, item_name in items:
                        total[key] = self._apis.get_common_data_with_repeat(tx_code, request_name, item_name)




            else:
                result = self._apis.get_common_data(tx_code, rc_name, repeat, item_name)

            key = generate_redis_key(tx_code, request_name)

            REDIS_SERVER.set(key, result)

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
