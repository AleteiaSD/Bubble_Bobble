import time

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject

from helpers.constants import BLOCK_SIZE


class Thread(QObject):
    signal = pyqtSignal(int)

    def __init__(self, sleep_period):
        super().__init__()
        self.x = BLOCK_SIZE
        self.y = BLOCK_SIZE
        self.velocity = None
        self.is_done = False
        self.sleep_period = sleep_period
        self.thread = QThread()

        self.moveToThread(self.thread)
        self.thread.started.connect(self.__start__)

    def start(self):
        self.thread.start()

    def setXY(self, x, y):
        self.x = x
        self.y = y

    def setVelocity(self, velocity):
        self.velocity = velocity

    def die(self):
        self.is_done = True
        self.thread.quit()

    @pyqtSlot()
    def __start__(self):
        while not self.is_done:
            self.signal.emit(self.x)
            time.sleep(self.sleep_period)
