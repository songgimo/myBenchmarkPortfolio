import inspect
import re

from PyQt5.QtCore import QObject

from modules.kiwoom.settings import *
from modules.global_settings import REDIS_SERVER, RedisKeys


class DynamicApis(object):
    def __init__(self, controller):
        self._dynamic_call = controller.dynamicCall

    def _create_request_name(self, code, item_korean):
        return '_'.join([code, item_korean])

    def set_value(self, name, value):
        return self._dynamic_call('SetInputValue(QString, QString)', name, value)

    def request_common_data(self, name, tx_code, screen_number, repeat):
        return self._dynamic_call('commRqData(QString, QString, int, QString)',
                                  [name, tx_code, repeat, screen_number])

    def common_request_data(self, code_list, repeat, code_list_length, n_type, request_name, screen_number):
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

    def get_code_list_by_markets(self, code_list):
        return self._dynamic_call("GetCodeListByMarket(QString)", code_list).split(';')

    def get_repeat_count(self, tx_code, request_name):
        return self._dynamic_call('GetRepeatCnt(QString, QString)', [tx_code, request_name])

    def get_stock_code_information(self, stock_code, item_name):
        # request_name = self._create_request_name(stock_code, item_name)

        self.set_value(ValueName.STOCK_CODE, stock_code)
        raw_data = self.request_common_data(item_name, OptCodes.STOCK_INFO, stock_code, IsRepeat.UNUSED)

        data = re.sub(r'[^\d]', '', raw_data) if raw_data.is_numeric() else raw_data

        return data


class KiwoomAPIModule(QObject):
    def __init__(self, controller):
        super(KiwoomAPIModule, self).__init__()

        self._controller = controller
        self._apis = DynamicApis(controller)

        self._receiver = Receiver(self._apis)

    def connect_block_list(self):
        pass

    def connect_real_list(self):
        pass

    def connect_block_tx_data(self):
        self.OnReceiveTrData.connect(self._receiver.blocking.get_tx_data)

    def connect_block_chejan_data(self):
        self.OnReceiveChejanData.connect(self._receiver.real.get_tx_data)

    def connect_block_message_data(self):
        self.OnReceiveMsg.connect(self._receiver.blocking.get_message)

    def get_stock_korean_name(self, stock_code):
        return self._apis.get_stock_code_information(stock_code, CustomItemName.STOCK_NAME)

    def get_stock_highest_price(self, stock_code):
        return self._apis.get_stock_code_information(stock_code, CustomItemName.HIGHEST_PRICE)

    def get_opening_price(self, stock_code):
        return self._apis.get_stock_code_information(stock_code, CustomItemName.OPENING_PRICE)

    def get_current_price(self, stock_code):
        return self._apis.get_stock_code_information(stock_code, CustomItemName.CURRENT_PRICE)


class Receiver(object):
    def __init__(self, apis):
        self.apis = apis
        self.blocking = self.Blocking(self)
        self.real = self.RealTime(self)

    class Blocking:
        def __init__(self, parent):
            self._apis = parent.apis

        def get_tx_data(self, *args):
            # get_common_data 이후 redis를 통한 통신
            screen_number, request_name, tx_code, rc_name, repeat, d_len, error_code, message, sp_message = args

            result = self._apis.get_common_data(tx_code, rc_name, repeat, request_name)

            # 실제로 사용하는 서버측에서 데이터 get해서 관련 데이터 추가로 가공한다.
            REDIS_SERVER.set(RedisKeys.TX_DATA, result)

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
