import math
from helpers.constants import *


def isCollision(element1, element2):
    distance = math.sqrt((math.pow(element1.x - element2.x, 2)) + math.pow(element1.y - element2.y, 2))
    return distance < BLOCK_SIZE


def isCollisionCoord(x1, y1, x2, y2):  # same function, but takes coordinates as arguments, instead of objects
    distance = math.sqrt((math.pow(x1 - x2, 2)) + math.pow(y1 - y2, 2))
    return distance < BLOCK_SIZE


def collisionPlayerEnemy(players, enemies, balloonEnemiesCollision):
    for p in range(len(players)):
        for e in range(len(enemies)):
            if isCollision(players[p], enemies[e]):
                if balloonEnemiesCollision:  # this will be indicator for collision between Balloons and Enemies
                    return p, e  # return index of each, for balloon and enemy collision, and for caught enemy and players
                else:
                    players[p].removeLife()

    return -1, -1


def collisionBuffOnBuff(newBuff, listOfBuffs):
    for b in range(len(listOfBuffs)):
        if isCollision(newBuff, listOfBuffs[b]):
            return True
    return False
