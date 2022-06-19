from PyQt5.QAxContainer import QAxWidget


class KiwoomCommunicator(Process):
    def __init__(self):
        super(KiwoomCommunicator, self).__init__()
        self._controller = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
