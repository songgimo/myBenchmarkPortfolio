from PyQt5.QAxContainer import QAxWidget
from modules.kiwoom.kiwoom import KiwoomAPIModule
from modules.global_settings import REDIS_SERVER, RedisKeys

from multiprocessing import Process


class KiwoomCommunicator(Process):
    def __init__(self):
        super(KiwoomCommunicator, self).__init__()
        self._controller = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        KiwoomAPIModule(self._controller).start()

    def run(self):
        while True:
            # KiwoomService에서 요청하는 함수값을 Serve
            try:
                request_command = REDIS_SERVER.get(RedisKeys.COM_COMMAND_KEY)
            except:
                continue

            REDIS_SERVER.set(RedisKeys.KIWOOM_API_KEY, request_command)
            try:
                result = REDIS_SERVER.get(RedisKeys.COM_TO_MODULE_RESULT_KEY)
                REDIS_SERVER.set(RedisKeys.COM_TO_SERVICE_RESULT_KEY, result)
            except:
                continue
