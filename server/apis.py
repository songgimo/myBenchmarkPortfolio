from modules.global_settings import REDIS_SERVER, RedisKeys
from win32com import client


class KiwoomApiService(object):
    def __init__(self):
        super(KiwoomApiService, self).__init__()
        self._controller = client.Dispatch("KHOPENAPI.KHOpenAPICtrl.1")

    def set_and_get_result(self, command):
        REDIS_SERVER.set(RedisKeys.KIWOOM_API_KEY, command)
        try:
            return REDIS_SERVER.get(RedisKeys.COM_TO_MODULE_RESULT_KEY)
        except:
            return dict()

    def get_all_stocks(self):
        pass

    def get_all_stocks_korean_name(self):
        pass
