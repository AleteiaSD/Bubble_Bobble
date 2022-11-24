from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QLabel
import time
from helpers.constants import *


class Player(QLabel):
    score = 0
    lives = 3
    name = " "
    buff = False
    velocity = 4 if buff is False else 8
    isJump = False
    isOnGround = True
    jumpCount = 6  # koliko visoko skacemo, ukljucujuci 0, dakle 7 iteracija -> 7 * (BLOCK SIZE / 2) = 3 kompletna BLOCK SIZE-a i preostala polovina za vizuelni efekat doskoka

    def __init__(self, label, x, y, playerId):
        super().__init__()
        self.label = label
        self.x = x
        self.y = y
        self.playerId = playerId
        self.currDir = playerId  # 1 is left, 2 is right
        self.immune = False
        self.lastDeath = time.time()
        self.lastBubble = 0

    def makeMove(self, direction, label):
        if direction == 'UP':
            # self.y -= 5 * self.velocity
            # self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
            self.y -= BLOCK_SIZE / 2
        elif direction == 'DOWN':
            self.y += 5 * self.velocity
        elif direction == 'RIGHT':
            # if self.currDir == 2:
            #     self.turnAround(label)
            #     self.currDir = 1
            self.x += 5 * self.velocity
        elif direction == 'LEFT':
            # if self.currDir == 1:
            #     self.turnAround(label)
            #     self.currDir = 2
            self.x -= 5 * self.velocity

        label.move(self.x, self.y)

    def turnAround(self, label):
        label.setPixmap(self.label.pixmap().transformed(QTransform().scale(-1, 1)))

    def checkImmunity(self):
        if self.lastDeath + IMMUNE_PERIOD < time.time():
            self.immune = False

    def canShoot(self):
        if self.lastBubble + BUBBLE_CREATION_PERIOD < time.time():
            self.lastBubble = time.time()
            return True
        else:
            return False

    def removeLife(self):
        if self.immune is False:
            self.lives -= 1
            self.x = BLOCK_SIZE if self.playerId == 1 else (WIDTH - BLOCK_SIZE * 2)
            self.y = HEIGHT - BLOCK_SIZE * 3
            self.label.move(self.x, self.y)
            self.immune = True
            self.lastDeath = time.time()

    def isDead(self):
        return self.lives <= 0
