from PyQt5.QtWidgets import QLabel

class CaughtEnemy(QLabel):

    def __init__(self, label, x, y, playerId):
        super().__init__()
        self.label = label
        self.caughtByPlayerWithId = playerId
        self.x = x
        self.y = y

    def MoveCaughtEnemy(self, label):
        label.move(self.x, self.y)
