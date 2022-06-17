import inspect

from PyQt5.QtCore import QObject

from modules.kiwoom.settings import *


class DynamicApis(object):
    def __init__(self, controller):
        self._dynamic_call = controller.dynamicCall

    def set_value(self, name, value):
        return self._dynamic_call('SetInputValue(QString, QString)', name, value)

    def request_common_data(self, name, tx_code, screen_number, repeat):
        return self._dynamic_call('commRqData(QString, QString, int, QString)',
                                  [name, tx_code, repeat, screen_number])

    def common_request_data(self, code_list, repeat, code_list_length, n_type, request_name, screen_number):
        return self._dynamic_call('CommKwRqData(QString, int, int, int, QString, QString)',
                                  [code_list, repeat, code_list_length, n_type, request_name, screen_number])

    def get_repeat_count(self, tx_code, request_name):
        return self._dynamic_call('GetRepeatCnt(QString, QString)', [tx_code, request_name])

    def send_order(self, request_name, screen_number, account, order_type, stock_code, quantity,
                   price, trade_type, origin_order_number):
        return self._dynamic_call('SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)',
                                  [request_name, screen_number, account, order_type, stock_code,
                                   quantity, price, trade_type, origin_order_number])

    def get_code_list_by_markets(self, code_list):
        return self._dynamic_call("GetCodeListByMarket(QString)", code_list).split(';')


class KiwoomAPIModule(QObject):
    def __init__(self, controller):
        super(KiwoomAPIModule, self).__init__()

        self._apis = DynamicApis(controller)

    def _create_request_name(self, code, item_korean):
        return '_'.join([code, item_korean])

    def get_stock_korean_name(self, stock_code):
        request_name = self._create_request_name(stock_code, CustomItemName.STOCK_NAME)

        self._apis.set_value(ValueName.STOCK_CODE, stock_code)
        self._apis.request_common_data(request_name, OptCodes.STOCK_INFO, stock_code, IsRepeat.UNUSED)

    def get_stock_highest_price(self, stock_code):
        request_name = self._create_request_name(stock_code, CustomItemName.HIGHEST_PRICE)

        self._apis.set_value(ValueName.STOCK_CODE, stock_code)
        self._apis.request_common_data(request_name, OptCodes.STOCK_INFO, self._stock_code, IsRepeat.UNUSED)

