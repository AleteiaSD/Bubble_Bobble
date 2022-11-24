
from PyQt5.QtWidgets import QLabel

from helpers.constants import *


class Bubble(QLabel):

    def __init__(self, label, direction, x, y, image, playerId):
        super().__init__()
        self.label = label
        self.image = image
        self.ShootByPlayerWithId = playerId
        self.initialX = x
        self.initialY = y
        self.x = x
        self.y = y
        self.currentDirection = direction

    def BubbleMove(self, label):
        if abs(self.x - self.initialX) < 4 * BLOCK_SIZE:
            if self.currentDirection == 1:  # Move left
                self.x += 2
                label.move(self.x, self.y)
            elif self.currentDirection == 2:  # Move right
                self.x -= 2
                label.move(self.x, self.y)
        else:
            self.y -= 2
            label.move(self.x, self.y)
