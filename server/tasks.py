from modules.global_settings import REDIS_SERVER, RedisKeys
from modules.kiwoom.settings import Commands, IsRepeat
from modules.utils import set_redis, get_redis
from server.queries import GetQueries

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

    def get_stocks_daily_candle_not_entered(self, data_set, date):
        for n, data in enumerate(data_set):
            if date in data:
                return data_set[:n]

    def get_all_daily_candle_by_stock_code(self, stock_code, latest_date):
        is_repeat = IsRepeat.NO
        total = []
        while True:
            result = self.set_and_get_result(
                Commands.GET_ALL_DAILY_CANDLE,
                code=stock_code,
                latest_date=latest_date,
                is_repeat=is_repeat
            )

            input_date = GetQueries.is_exist_table_by_stock_code(stock_code)  # timestamp
            if input_date:
                not_entered = self.get_stocks_daily_candle_not_entered(result['total'], input_date[0][0])
                if not_entered:
                    total += not_entered
                return total

            # 반복시 마지막 날짜를 기준으로 가져오므로
            if is_repeat == IsRepeat.YES:
                # 반복 상태가 아닌 경우 수집 종료.
                total += result['total']
                return total

            total += result['total'][:-1]

    def get_history_price_all_stocks(self):
        codes = self.set_and_get_result(Commands.GET_ALL_KOREAN_STOCK_CODE)

        latest_date = (datetime.datetime.now() - datetime.timedelta(days=1))
        result = dict()
        for code in codes:
            total_result = self.get_all_daily_candle_by_stock_code(code, latest_date)
            result[code] = total_result

        return result
