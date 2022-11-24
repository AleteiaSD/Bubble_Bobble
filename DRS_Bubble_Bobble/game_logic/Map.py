from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtWidgets import QFrame

from helpers.constants import *


def __draw__(x, y, painter):
    painter.drawRect(x, y, BLOCK_SIZE, BLOCK_SIZE)


class Map(QFrame):
    upperY = -1

    def __init__(self, parent, index):
        super().__init__(parent)
        self.levelIndex = index % len(Levels)

    def obstacles(self):
        Walls = []
        level = Levels[self.levelIndex]
        for x in range(len(level)):
            for y in range(len(level[x])):
                character = level[x][y]
                if character == "X" or character == "Y":
                    coordX = x * BLOCK_SIZE
                    coordY = y * BLOCK_SIZE
                    Walls.append((coordY, coordX))
                    if character == "Y":
                        self.upperY = y
        return Walls

    def paintEvent(self, event):
        tileBrush = QBrush(QColor(COLORS[self.levelIndex]))
        pen = QPen(Qt.black, 0.5)
        painter = QPainter(self)
        painter.setBrush(tileBrush)
        painter.setPen(pen)
        w = self.obstacles()
        for x, y in w:
            __draw__(x, y, painter)


Levels = [["XXXXXXXYXXXXXXXXXXXX",
           "X                  X",
           "X                  X",
           "XXXXX    XX    XXXXX",
           "X     X      X     X",
           "X                  X",
           "X X     XXXX     X X",
           "X                  X",
           "X                  X",
           "X    XXXXXXXXXX    X",
           "X                  X",
           "X                  X",
           "XXXX   XXXXXX   XXXX",
           "X        XX        X",
           "X                  X",
           "XXXXXXXXXXXXXXXXXXXX"],

          ["XXXXXXXXYXXXXXXXXXXX",
           "X                  X",
           "X                  X",
           "XXXXXXX      XXXXXXX",
           "X        XX        X",
           "X                  X",
           "XXX    X    X    XXX",
           "X      X    X      X",
           "X                  X",
           "X   XXXXXXXXXXXX   X",
           "X                  X",
           "X                  X",
           "XXX    XXXXXX    XXX",
           "X                  X",
           "X                  X",
           "XXXXXXXXXXXXXXXXXXXX"]]
