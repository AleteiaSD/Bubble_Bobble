from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QLabel

from game_logic.Map import Map
from helpers.constants import *


class Enemy(QLabel):
    velocity = 1

    def __init__(self, label, x, y, image, currLevel):
        super().__init__()
        self.label = label
        self.image = image
        self.x = x
        self.y = y
        self.currDir = 2
        self.map = Map(self, currLevel)

    def move(self, label, playerX, playerY):
        if abs(self.y - playerY) >= BLOCK_SIZE // 2:
            if playerY > self.y:
                self.y += 1 * self.velocity
            elif playerY < self.y:
                self.y -= 1 * self.velocity
        if abs(self.x - playerX) >= BLOCK_SIZE // 2:
            if playerX > self.x:
                if self.currDir == 2:
                    self.turnAround(label)
                    self.currDir = 1
                self.x += 1 * self.velocity
            elif playerX < self.x:
                if self.currDir == 1:
                    self.turnAround(label)
                    self.currDir = 2
                self.x -= 1 * self.velocity
        label.move(self.x, self.y)

    def move_on_tile(self, label):
        self.checkRouteX(label)
        self.checkRouteY(label)
        if self.currDir == 1:
            self.x += 1 * self.velocity
        else:
            self.x -= 1 * self.velocity

        label.move(self.x, self.y)

    def checkRouteX(self, label):
        obstacles = self.map.obstacles()
        for (x, y) in obstacles:
            if self.currDir == 1:
                if abs(x - (self.x + 1 * self.velocity)) <= BLOCK_SIZE and y == self.y:
                    self.currDir = 2
                    self.turnAround(label)
            elif self.currDir == 2:
                if abs(x + (self.x - 1 * self.velocity)) <= BLOCK_SIZE and y == self.y:
                    self.currDir = 1
                    self.turnAround(label)

    def checkRouteY(self, label):
        obstacles = self.map.obstacles()
        dontMove = False
        z = self.x - (self.x % 40) + BLOCK_SIZE
        g = self.y + BLOCK_SIZE

        c = self.x // 40 * BLOCK_SIZE
        v = self.y + BLOCK_SIZE
        if self.currDir == 1:
            for item in obstacles:
                if (z, g) == item:
                    dontMove = True
        elif self.currDir == 2:
            for item in obstacles:
                if (c, v) == item:
                    dontMove = True

        if not dontMove:
            if self.currDir == 1:
                self.currDir = 2
            else:
                self.currDir = 1
            self.turnAround(label)

    def turnAround(self, label):
        label.setPixmap(self.label.pixmap().transformed(QTransform().scale(-1, 1)))
