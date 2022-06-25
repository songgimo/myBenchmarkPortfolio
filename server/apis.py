from modules.global_settings import REDIS_SERVER, RedisKeys
from modules.kiwoom.settings import Commands
from win32com import client


class KiwoomApiService(object):
    def __init__(self):
        super(KiwoomApiService, self).__init__()
        self._controller = client.Dispatch("KHOPENAPI.KHOpenAPICtrl.1")

        # connection for getting data.
        self.set_and_get_result(Commands.CONNECT_ALL_BLOCK)
        self.set_and_get_result(Commands.CONNECT_ALL_REAL)

    def set_and_get_result(self, command):
        REDIS_SERVER.set(RedisKeys.KIWOOM_API_KEY, command)
        try:
            return REDIS_SERVER.get(RedisKeys.COM_TO_MODULE_RESULT_KEY)
        except:
            return dict()

    def get_all_stocks(self):
        self.set_and_get_result(Commands.GET_ALL_KOREAN_STOCK_CODE)

    def get_all_stocks_korean_name(self):
        pass
