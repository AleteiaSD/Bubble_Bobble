from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
import random
from helpers.constants import *


class BuffDebuffPoints(QLabel):

    def __init__(self, label, x, y, lives):
        super().__init__()
        self.lives = lives
        self.picture
        self.label = label
        self.setPicture()
        self.label.setPixmap(QPixmap(self.picture).scaled(BLOCK_SIZE, BLOCK_SIZE))
        self.label.setStyleSheet("background:transparent")
        self.label.resize(BLOCK_SIZE, BLOCK_SIZE)

        self.x = x
        self.y = y

    def generateResult(self, player):
        if self.lives:
            buff = random.choice(RANDOM_BUFF_LIVES)
            if buff == "LIVES_DOWN":
                player.removeLife()
            elif buff == "LIVES_UP":
                player.lives += 1
        else:
            buff = random.choice(RANDOM_BUFF_POINTS)
            if buff == "POINTS_UP":
                player.score += 10
            else:
                if player.score >= 10:
                    player.score -= 10
                else:
                    player.score += 10

    def setPicture(self):
        if self.lives:
            self.picture = "resource/heart.png"
        else:
            self.picture = "resource/buff.png"
