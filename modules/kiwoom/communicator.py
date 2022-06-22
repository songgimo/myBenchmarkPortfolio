from PyQt5.QAxContainer import QAxWidget
from PyQt5 import QtCore
from modules.kiwoom.kiwoom import KiwoomAPIModule
from multiprocessing import Process
from modules.global_settings import REDIS_SERVER, RedisKeys
from modules.kiwoom.settings import Commands


class KiwoomCommunicator(QtCore.QThread):
    def __init__(self):
        super(KiwoomCommunicator, self).__init__()
        self._controller = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        KiwoomAPIModule(self._controller).start()

    def run(self):
        while True:
            REDIS_SERVER.set(RedisKeys.KIWOOM_API_KEY, Commands.GET_STOCK_KOREAN_NAME)
