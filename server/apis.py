from modules.global_settings import REDIS_SERVER, RedisKeys
from modules.kiwoom.settings import Commands, IsRepeat
from modules.utils import set_redis, get_redis

from win32com import client

import threading
import datetime


class KiwoomApiService(object):
    def __init__(self):
        super(KiwoomApiService, self).__init__()
        self._controller = client.Dispatch("KHOPENAPI.KHOpenAPICtrl.1")

        # connection for getting data.
        self.set_and_get_result(Commands.CONNECT_ALL_BLOCK)
        self.set_and_get_result(Commands.CONNECT_ALL_REAL)

    def set_and_get_result(self, command, **kwargs):
        parameters = {
            "command": command,
            "kwargs": kwargs
        }
        set_redis(RedisKeys.Kiwoom.API_KEY, parameters)
        try:
            return get_redis(RedisKeys.Kiwoom.COM_TO_MODULE_RESULT_KEY)
        except:
            return dict()

    def get_history_price_all_stocks(self):
        codes = self.set_and_get_result(Commands.GET_ALL_KOREAN_STOCK_CODE)

        latest_date = (datetime.datetime.now() - datetime.timedelta(days=1))
        for code in codes:
            result = self.set_and_get_result(
                Commands.GET_ALL_DAILY_CANDLE,
                code=code,
                latest_date=latest_date,
                is_repeat=IsRepeat.NO
            )

            if result['repeat'] == IsRepeat.YES:
                pass

    def get_all_stocks_korean_name(self):
        pass
