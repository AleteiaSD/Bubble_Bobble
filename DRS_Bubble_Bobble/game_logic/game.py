import random
import time
from multiprocessing import Queue
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QMessageBox

from game_logic import Collision
from game_logic.Bubble import Bubble
from game_logic.BuffDebuff import BuffDebuffPoints
from game_logic.CaughtEnemy import CaughtEnemy
from game_logic.Enemy import Enemy
from game_logic.Map import Map
from game_logic.Player import Player
from helpers.CustomThread import Thread
from helpers.Key_Notifier import KeyNotifier
from helpers.constants import *


class Game(QMainWindow):

    def __init__(self, queue: Queue, numOfPlayers, name1="Player1", name2="Player2", level=1, score1=0, score2=0,
                 velocity=1):
        super().__init__()
        self.queue = queue
        self.numOfPlayers = numOfPlayers
        self.level = level
        self.enemyVelocity = velocity
        self.map = Map(self, self.level)
        self.__initUI()
        self.__initPlayer(score1, score2, name1, name2)
        self.__initEnemy()
        self.winner = ""
        self.timeForBuff = True
        self.spawnCheck = 5
        self.lastMade = time.time()
        self.isCreatedBalloon = False
        self.listForBalloons = []
        self.listForCaughtEnemies = []
        self.listForBuffs = []

        # self.show()

    def start(self):
        self.show()
        self.movementNotifier = KeyNotifier(PLAYER_MOVEMENT_PERIOD)
        self.movementNotifier.key_signal.connect(self.__updatePosition)
        self.movementNotifier.start()

        self.enemyThread = Thread(ENEMY_MOVEMENT_PERIOD)
        self.enemyThread.signal.connect(self.__updateEnemy)
        self.enemyThread.start()

        self.bubbleThread = Thread(BUBBLE_MOVEMENT_PERIOD)
        self.bubbleThread.signal.connect(self.__updateBubble)
        self.bubbleThread.start()

        self.buffThread = Thread(BUFF_CHECK_PERIOD)
        self.buffThread.signal.connect(self.__generateBuff)
        self.buffThread.start()

        self.gravityThread = Thread(GRAVITY_CHECK_PERIOD)
        self.gravityThread.signal.connect(self.__GravityForPlayers)
        self.gravityThread.start()

        self.jumpingThread = Thread(JUMP_CHECK_PERIOD)
        self.jumpingThread.signal.connect(self.__JumpingForPlayers)
        self.jumpingThread.start()

    def __initUI(self):
        self.setWindowTitle('Bubble Bobble ' + ('single player' if self.numOfPlayers == 1 else 'multiplayer'))
        self.setWindowIcon(QIcon('resource/player1.png'))
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)
        self.setStyleSheet("background-color: black;")
        self.setCentralWidget(self.map)

        self.banner = QLabel(self)
        self.banner.move(250, HEIGHT - BLOCK_SIZE)
        self.banner.resize(600, BLOCK_SIZE)
        self.banner.setText(f'BUBBLE BOBBLE game | Level: {self.level}')
        self.banner.setStyleSheet(f"color: aqua; font-size: 18px; font-style: bold")
        self.banner.show()

    def __initPlayer(self, score1, score2, name1, name2):

        self.players = []
        self.player1_label = QLabel(self)
        self.player1_label.setPixmap(QPixmap("resource/player1.png").scaled(BLOCK_SIZE, BLOCK_SIZE))
        self.player1_label.setStyleSheet("background:transparent;")
        self.player1_label.resize(BLOCK_SIZE, BLOCK_SIZE)
        x, y = [BLOCK_SIZE, HEIGHT - BLOCK_SIZE * 3]
        self.player1 = Player(self.player1_label, x, y, 1)
        self.player1_label.move(x, y)
        self.player1.score = score1
        self.player1.name = name1
        self.players.append(self.player1)

        self.Ply1Score = QLabel(self)
        self.Ply1Score.move(0, HEIGHT - BLOCK_SIZE)
        self.Ply1Score.resize(180, 40)
        self.Ply1Score.setStyleSheet("background-color: gray; font-size: 16px")
        self.Ply1Score.setContentsMargins(10, 0, 0, 0)
        self.Ply1Score.show()

        if self.numOfPlayers == 2:
            self.player2_label = QLabel(self)
            self.player2_label.setPixmap(QPixmap("resource/player2.png").scaled(BLOCK_SIZE, BLOCK_SIZE))
            self.player2_label.setStyleSheet("background:transparent")
            self.player2_label.resize(BLOCK_SIZE, BLOCK_SIZE)
            x, y = [WIDTH - BLOCK_SIZE * 2, HEIGHT - BLOCK_SIZE * 3]
            self.player2 = Player(self.player2_label, x, y, 2)
            self.player2_label.move(x, y)
            self.player2.score = score2
            self.player2.name = name2
            self.players.append(self.player2)

            self.Ply2Score = QLabel(self)
            self.Ply2Score.move(WIDTH - 180, HEIGHT - BLOCK_SIZE)
            self.Ply2Score.resize(180, 40)
            self.Ply2Score.setStyleSheet("background-color: gray; font-size: 16px")
            self.Ply2Score.setContentsMargins(10, 0, 0, 0)
            self.Ply2Score.show()

    def __initEnemy(self):
        self.enemies = []
        if self.level > STRONG_ENEMY_LEVEL_REQUIREMENT:
            self.enemy_label = QLabel(self)
            picture = "resource/enemy1.png"
            self.enemy_label.setPixmap(QPixmap(picture).scaled(BLOCK_SIZE, BLOCK_SIZE))
            self.enemy_label.resize(BLOCK_SIZE, BLOCK_SIZE)
            x, y = [random.randint(BLOCK_SIZE, WIDTH - BLOCK_SIZE), BLOCK_SIZE]
            self.enemy_label.setStyleSheet("background:transparent")
            self.enemy = Enemy(self.enemy_label, x, y, picture, self.level)
            self.enemy_label.move(x, y)
            self.enemies.append(self.enemy)

            if self.numOfPlayers == 2:
                self.enemy_label2 = QLabel(self)
                picture = "resource/enemy2.png"
                self.enemy_label2.setPixmap(QPixmap(picture).scaled(BLOCK_SIZE, BLOCK_SIZE))
                self.enemy_label2.resize(BLOCK_SIZE, BLOCK_SIZE)
                x, y = [random.randint(BLOCK_SIZE, WIDTH - BLOCK_SIZE), BLOCK_SIZE]
                self.enemy_label2.setStyleSheet("background:transparent")
                self.enemy2 = Enemy(self.enemy_label2, x, y, picture, self.level)
                self.enemy_label2.move(x, y)
                self.enemies.append(self.enemy2)

        self.simple_enemy_label = QLabel(self)
        picture = random.choice(["resource/simple_enemy1.png", "resource/simple_enemy2.png"])
        self.simple_enemy_label.setPixmap(QPixmap(picture).scaled(BLOCK_SIZE, BLOCK_SIZE))
        self.simple_enemy_label.resize(BLOCK_SIZE, BLOCK_SIZE)
        x, y = [BLOCK_SIZE, BLOCK_SIZE * 2]
        self.simple_enemy_label.setStyleSheet("background:transparent")
        self.simple_enemy = Enemy(self.simple_enemy_label, x, y, picture, self.level)
        self.simple_enemy_label.move(x, y)
        self.enemies.append(self.simple_enemy)

        self.simple_enemy_label2 = QLabel(self)
        picture = random.choice(["resource/simple_enemy1.png", "resource/simple_enemy2.png"])
        self.simple_enemy_label2.setPixmap(QPixmap(picture).scaled(BLOCK_SIZE, BLOCK_SIZE))
        self.simple_enemy_label2.resize(BLOCK_SIZE, BLOCK_SIZE)
        x, y = [BLOCK_SIZE * 18, BLOCK_SIZE * 2]
        self.simple_enemy_label2.setStyleSheet("background:transparent")
        self.simple_enemy2 = Enemy(self.simple_enemy_label2, x, y, picture, self.level)
        self.simple_enemy_label2.move(x, y)
        self.enemies.append(self.simple_enemy2)

        self.simple_enemy_label3 = QLabel(self)
        picture = random.choice(["resource/simple_enemy1.png", "resource/simple_enemy2.png"])
        self.simple_enemy_label3.setPixmap(QPixmap(picture).scaled(BLOCK_SIZE, BLOCK_SIZE))
        self.simple_enemy_label3.resize(BLOCK_SIZE, BLOCK_SIZE)
        x, y = [BLOCK_SIZE * 4, BLOCK_SIZE * 8]
        self.simple_enemy_label3.setStyleSheet("background:transparent")
        self.simple_enemy3 = Enemy(self.simple_enemy_label3, x, y, picture, self.level)
        self.simple_enemy_label3.move(x, y)
        self.enemies.append(self.simple_enemy3)

        for e in self.enemies:
            e.velocity *= self.enemyVelocity

    def __initBuffDebuff(self):
        x, y = BLOCK_SIZE * random.randint(1, 18), BLOCK_SIZE * random.randint(1, 11)
        self.buff_type = random.choice(RANDOM_BUFF_TYPE)
        self.buff_label = QLabel(self)

        if self.buff_type == RANDOM_BUFF_TYPE[1]:
            self.buff = BuffDebuffPoints(self.buff_label, x, y, False)
        elif self.buff_type == RANDOM_BUFF_TYPE[0]:
            self.buff = BuffDebuffPoints(self.buff_label, x, y, True)

        self.buff_label.move(x, y)

        if len(self.listForBuffs) < 3:
            if not Collision.collisionBuffOnBuff(self.buff, self.listForBuffs) and self.__isValidMove([0, 0],
                                                                                                      self.buff_label):
                self.spawnCheck = random.randint(BUFF_SPAWN_PERIOD[0], BUFF_SPAWN_PERIOD[1])

                self.buff_label.show()
                self.lastMade = time.time()
                self.listForBuffs.append(self.buff)

    def __generateBuff(self):
        if self.timeForBuff:
            self.timeForBuff = False
            self.__initBuffDebuff()

        if self.lastMade + self.spawnCheck < time.time():
            self.timeForBuff = True

        self.__upadateBuff()

    def __upadateBuff(self):
        indexPlayer, indexBuff = Collision.collisionPlayerEnemy(self.players, self.listForBuffs,
                                                                balloonEnemiesCollision=True)
        if indexPlayer != -1 and indexBuff != -1:
            if self.listForBuffs[indexBuff].lives:
                if not self.players[indexPlayer].immune:
                    self.listForBuffs[indexBuff].label.hide()
                    self.listForBuffs[indexBuff].generateResult(self.players[indexPlayer])
                    del self.listForBuffs[indexBuff]
            else:
                self.listForBuffs[indexBuff].label.hide()
                self.listForBuffs[indexBuff].generateResult(self.players[indexPlayer])
                del self.listForBuffs[indexBuff]

    def __JumpingForPlayers(self):
        for player in self.players:
            if player.isJump:
                if player.jumpCount >= 0:
                    if player.y > self.map.upperY + BLOCK_SIZE:
                        player.makeMove('UP', player.label)
                        player.jumpCount -= 1
                        player.isOnGround = False
                    else:
                        player.jumpCount = 6
                        player.isJump = False
                else:
                    player.jumpCount = 6
                    player.isJump = False

    def __GravityForPlayers(self):
        for player in self.players:
            if not player.isJump:  # ako ne skace primeni gravitaciju
                if self.__isValidMove([0, BLOCK_SIZE / 2], player.label):
                    player.makeMove('DOWN', player.label)
                    player.isOnGround = False
                else:
                    player.isOnGround = True

    def keyPressEvent(self, event):

        if event.key() in KeyMappingPlayer1 or event.key() in KeyMappingPlayer2:
            self.movementNotifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        # without this condition, keyReleaseEvent can mess up if use a key which isn't related to an action
        if event.key() in KeyMappingPlayer1 or event.key() in KeyMappingPlayer2:
            self.movementNotifier.rem_key(event.key())

    def closeEvent(self, event):
        self.movementNotifier.die()
        self.enemyThread.die()
        self.bubbleThread.die()
        self.gravityThread.die()
        self.jumpingThread.die()

    def __CreateBubble(self, key):
        if key in KeyMappingPlayer1 and KeyMappingPlayer1[key] == 'SHOOT' and self.player1.canShoot():
            self.bubble_label = QLabel(self)
            self.bubble_label.setStyleSheet("background:transparent")
            self.bubble_label.resize(BLOCK_SIZE, BLOCK_SIZE)
            x, y = self.player1.x + BLOCK_SIZE, self.player1.y
            image = "resource/balloon2.png"
            self.bubble_label.setPixmap(QPixmap(image).scaled(BLOCK_SIZE, BLOCK_SIZE))
            if self.player1.currDir == 2:  # if player is turned right draw bubble in his direction
                x = self.player1.x - BLOCK_SIZE
            self.bubble = Bubble(self.bubble_label, self.player1.currDir, x, y, image, self.player1.playerId)
            self.bubble_label.move(x, y)
            self.bubble_label.show()
            self.listForBalloons.append(self.bubble)
            self.isCreatedBalloon = True

        elif key in KeyMappingPlayer2 and KeyMappingPlayer2[key] == 'SHOOT' and self.player2.canShoot():
            self.bubble_label = QLabel(self)
            self.bubble_label.setStyleSheet("background:transparent")
            self.bubble_label.resize(BLOCK_SIZE, BLOCK_SIZE)
            x, y = self.player2.x + BLOCK_SIZE, self.player2.y
            image = "resource/balloon1.png"
            self.bubble_label.setPixmap(QPixmap(image).scaled(BLOCK_SIZE, BLOCK_SIZE))
            if self.player2.currDir == 2:  # if player is turned right draw bubble in his direction
                x = self.player2.x - BLOCK_SIZE
            self.bubble = Bubble(self.bubble_label, self.player2.currDir, x, y, image, self.player2.playerId)
            self.bubble_label.move(x, y)
            self.bubble_label.show()
            self.listForBalloons.append(self.bubble)
            self.isCreatedBalloon = True

    def __FindPictureForEnemyAndBalloon(self, imageEnemy, imageBalloon):
        for key, value in MappingPicturesOfEnemiesAndBalloons.items():
            if key == (imageBalloon, imageEnemy):
                return value

    def __CreateLabelForCaughtEnemy(self, enemy, balloon):
        self.label_caughtEnemy = QLabel(self)
        picture = self.__FindPictureForEnemyAndBalloon(enemy.image, balloon.image)
        self.label_caughtEnemy.setPixmap(QPixmap(picture).scaled(BLOCK_SIZE * 1.25, BLOCK_SIZE))
        self.label_caughtEnemy.setStyleSheet("background:transparent")
        self.label_caughtEnemy.resize(BLOCK_SIZE * 1.25, BLOCK_SIZE)
        self.label_caughtEnemy.move(enemy.x, enemy.y)

        if not self.__isValidMove([0, 0], self.label_caughtEnemy):
            direction, steps = self.FindShortestPathForCaughtEnemy(self.label_caughtEnemy, enemy.x, enemy.y)
            if direction == 'up':
                self.label_caughtEnemy.move(enemy.x, (enemy.y - ((BLOCK_SIZE / 2) * steps)))
            elif direction == 'down':
                self.label_caughtEnemy.move(enemy.x, (enemy.y + ((BLOCK_SIZE / 2) * steps)))
            elif direction == 'left':
                self.label_caughtEnemy.move((enemy.x - ((BLOCK_SIZE / 2) * steps)), enemy.y)
            elif direction == 'right':
                self.label_caughtEnemy.move((enemy.x + ((BLOCK_SIZE / 2) * steps)), enemy.y)

        self.label_caughtEnemy.show()
        self.CaughtEnemy = CaughtEnemy(self.label_caughtEnemy, self.label_caughtEnemy.x(), self.label_caughtEnemy.y(),
                                       balloon.ShootByPlayerWithId)
        self.listForCaughtEnemies.append(self.CaughtEnemy)

    def FindShortestPathForCaughtEnemy(self, labelCaughtEnemy, enemyX, enemyY):

        label = QLabel(self)
        label.move(labelCaughtEnemy.x(), labelCaughtEnemy.y())
        directions = ['up', 'down', 'left', 'right']
        counterUP, counterLEFT, counterRIGHT, counterDOWN = 0, 0, 0, 0
        x, y = enemyX, enemyY
        for direction in directions:
            while not self.__isValidMove([0, 0], label):
                if direction == 'down':
                    y += BLOCK_SIZE // 2
                    counterDOWN += 1
                elif direction == 'up':
                    y -= BLOCK_SIZE // 2
                    counterUP += 1
                elif direction == 'left':
                    x -= BLOCK_SIZE // 2
                    counterLEFT += 1
                elif direction == 'right':
                    x += BLOCK_SIZE // 2
                    counterRIGHT += 1
                label.move(x, y)
            # end while -> move label to start position,
            label.move(labelCaughtEnemy.x(), labelCaughtEnemy.y())
            x, y = enemyX, enemyY  # reset coordinates

        lista = [('up', counterUP), ('down', counterDOWN), ('left', counterLEFT), ('right', counterRIGHT)]
        sortirani = sorted(lista, key=lambda tup: tup[1])  # sort(asc) by counter
        del label
        return sortirani[0]  # return direction with lowest counter

    def __isValidMove(self, delta, label):
        newX, newY = delta[0] + label.x(), delta[1] + label.y()
        obstacles = self.map.obstacles()
        for (x, y) in obstacles:
            if abs(x - newX) <= BLOCK_SIZE // 2 and abs(y - newY) <= BLOCK_SIZE // 2:
                return False
        return True

    def __updatePosition(self, key):
        # if key == QtCore.Qt.Key_Space:
        #     self.__CreateBubble(key)
        if key in KeyMappingPlayer1:  # and self.__isValidMove(Moves[KeyMappingPlayer1[key]], self.player1_label):
            if KeyMappingPlayer1[key] == 'SHOOT':
                self.__CreateBubble(key)
            elif KeyMappingPlayer1[key] == 'UP':
                if self.player1.isOnGround: # onemogucen dupli skok
                    self.player1.isJump = True
            else:
                self.CheckForTurningAround(self.player1, key)
                if self.__isValidMove(Moves[KeyMappingPlayer1[key]], self.player1.label):
                    self.player1.makeMove(KeyMappingPlayer1[key], self.player1_label)

        if self.numOfPlayers == 2:
            if key in KeyMappingPlayer2:  # and self.__isValidMove(Moves[KeyMappingPlayer2[key]], self.player2_label):
                if KeyMappingPlayer2[key] == 'SHOOT':
                    self.__CreateBubble(key)
                elif KeyMappingPlayer2[key] == 'UP':
                    if self.player2.isOnGround: # onemogucen dupli skok
                        self.player2.isJump = True
                else:
                    self.CheckForTurningAround(self.player2, key)
                    if self.__isValidMove(Moves[KeyMappingPlayer2[key]], self.player2_label):
                        self.player2.makeMove(KeyMappingPlayer2[key], self.player2_label)

    def CheckForTurningAround(self, player, key):
        if key in KeyMappingPlayer1:
            if KeyMappingPlayer1[key] == 'RIGHT' and player.currDir == 2:
                player.turnAround(player.label)
                player.currDir = 1
            elif KeyMappingPlayer1[key] == 'LEFT' and player.currDir == 1:
                player.turnAround(player.label)
                player.currDir = 2
        elif key in KeyMappingPlayer2:
            if KeyMappingPlayer2[key] == 'RIGHT' and player.currDir == 2:
                player.turnAround(player.label)
                player.currDir = 1
            elif KeyMappingPlayer2[key] == 'LEFT' and player.currDir == 1:
                player.turnAround(player.label)
                player.currDir = 2

    def __updateEnemy(self):
        if self.level > STRONG_ENEMY_LEVEL_REQUIREMENT:
            self.enemy.move(self.enemy_label, self.player1.x, self.player1.y)
            if self.numOfPlayers == 2:
                self.enemy2.move(self.enemy_label2, self.player2.x, self.player2.y)
        self.simple_enemy.move_on_tile(self.simple_enemy_label)
        self.simple_enemy2.move_on_tile(self.simple_enemy_label2)
        self.simple_enemy3.move_on_tile(self.simple_enemy_label3)
        Collision.collisionPlayerEnemy(players=self.players, enemies=self.enemies, balloonEnemiesCollision=False)

    def __updateBubble(self):
        if self.isCreatedBalloon:
            lista = []
            for index in range(len(self.listForBalloons)):
                if self.listForBalloons[index].y <= 0 or self.listForBalloons[index].x <= 0 or self.listForBalloons[index].x >= WIDTH:
                    # add to list balloons that are invisible in main window, they will be deleted later
                    self.listForBalloons[index].label.hide()
                    lista.append(index)
                else:
                    self.listForBalloons[index].BubbleMove(self.listForBalloons[index].label)

            # delete from list every invisible balloon
            for item in lista:
                if item in self.listForBalloons:
                    self.listForBalloons[item].label.hide()
                    del self.listForBalloons[item]

        indexOfBalloon, indexOfEnemy = Collision.collisionPlayerEnemy(self.listForBalloons, self.enemies,
                                                                      balloonEnemiesCollision=True)
        if indexOfBalloon != -1 and indexOfEnemy != -1:
            self.__CreateLabelForCaughtEnemy(self.enemies[indexOfEnemy], self.listForBalloons[indexOfBalloon])
            self.enemies[indexOfEnemy].label.hide()
            del self.enemies[indexOfEnemy]
            self.listForBalloons[indexOfBalloon].label.hide()
            del self.listForBalloons[indexOfBalloon]

        indexOfPlayer, indexOfCaughtEnemy = Collision.collisionPlayerEnemy(self.players, self.listForCaughtEnemies,
                                                                           balloonEnemiesCollision=True)
        if indexOfPlayer != -1 and indexOfCaughtEnemy != -1:
            if self.players[indexOfPlayer].playerId == self.listForCaughtEnemies[indexOfCaughtEnemy].caughtByPlayerWithId:
                self.players[indexOfPlayer].score += 10
                self.listForCaughtEnemies[indexOfCaughtEnemy].label.hide()
                del self.listForCaughtEnemies[indexOfCaughtEnemy]
                # ovde moze i provera da li je simple ili onaj drugi enemy pa da se na osnovu toga
                # dodeli broj bodova npr. simple -> score += score ;  special enemy = score * 2
                # caught enemy dodati samo da ima svoju sliku pa na osnovu nje se to moze dodeliti

        self.__updateScore()
        self.__CheckGameOver()

    def __updateScore(self):
        self.banner.setText(f'BUBBLE BOBBLE game | Level: {self.level}')

        def immunityText(status):
            return 'Immune' if status is True else 'Not Immune'

        def immunityColor(status):
            return 'green' if status is True else 'red'

        self.player1.checkImmunity()
        self.Ply1Score.setText(
            f'{self.player1.name}: {self.player1.score}\nLives: {self.player1.lives} ({immunityText(self.player1.immune)})')
        self.Ply1Score.setStyleSheet(f'background-color: {immunityColor(self.player1.immune)}; font-size: 16px')
        if self.numOfPlayers == 2:
            self.player2.checkImmunity()
            self.Ply2Score.setText(
                f'{self.player2.name}: {self.player2.score}\nLives: {self.player2.lives} ({immunityText(self.player2.immune)})')
            self.Ply2Score.setStyleSheet(f'background-color: {immunityColor(self.player2.immune)}; font-size: 16px')

    def writeWinner(self):
        f = open('winner.txt', 'w+')
        f.write(self.winner)
        f.close()

    def __CheckGameOver(self):

        if self.numOfPlayers == 1:
            if self.player1.isDead():
                self.gameOverText = 'You died :(\n'
                self.gameOverText += f'Your score: {self.player1.score}'
                self.__GameOver()
            elif len(self.listForCaughtEnemies) == 0 and len(self.enemies) == 0:
                self.gameOverText = 'All enemies cleared!\n'
                self.gameOverText += f'Your score: {self.player1.score}\n'
                self.gameOverText += f'Lives left: {self.player1.lives}'
                self.__GameOver()
        elif self.numOfPlayers == 2:
            if self.player1.isDead():
                self.gameOverText = self.player1.name + '  died :(\n'  # TODO: add player names
                self.gameOverText += 'The winner is ' + self.player2.name + '!'
                self.winner += self.player2.name
                self.writeWinner()
                self.__GameOver()
            elif self.player2.isDead():
                self.gameOverText = self.player2.name + ' died :(\n'
                self.gameOverText += 'The winner is ' + self.player1.name + '!'
                self.winner += self.player1.name
                self.writeWinner()
                self.__GameOver()
            elif len(self.listForCaughtEnemies) == 0 and len(self.enemies) == 0:
                self.gameOverText = 'All enemies cleared!\n'
                self.gameOverText += self.player1.name + \
                                     f' score: {self.player1.score} ({self.player1.lives} lives left)\n'
                self.gameOverText += self.player2.name + \
                                     f' score: {self.player2.score} ({self.player2.lives} lives left)\n'
                self.gameOverText += self.__determineWinner()
                self.__GameOver()

    def __determineWinner(self):

        if self.player1.score > self.player2.score:
            return 'The winner is:' + self.player1.name
        elif self.player1.score < self.player2.score:
            return 'The winner is:' + self.player2.name
        else:
            if self.player1.lives > self.player2.lives:
                return 'The winner is:' + self.player1.name
            elif self.player1.lives < self.player2.lives:
                return 'The winner is:' + self.player2.name
            else:
                return 'It\'s a tie!'

    def __GameOver(self):
        msg = QMessageBox()
        msg.setWindowIcon(QIcon('resource/player1.png'))
        msg.setWindowTitle('Game over!\t\t')  # \t hackish way of adding width to messagebox
        msg.setText(self.gameOverText)
        msg.addButton(QMessageBox.Cancel)
        btnNextLvl = None
        if 'died' not in self.gameOverText:  # if no one died, we go to next lvl
            btnNextLvl = msg.addButton('Next Level', msg.ActionRole)

        self.setEnabled(False)
        self.movementNotifier.die()
        self.enemyThread.die()
        self.bubbleThread.die()
        self.buffThread.die()
        self.Ply1Score.setStyleSheet('background: gray')
        if self.numOfPlayers == 2:
            self.Ply2Score.setStyleSheet('background: gray')
        msg.exec_()

        if btnNextLvl is not None and msg.clickedButton() == btnNextLvl:
            self.close()
            self.__NextLevel()
        else:
            self.close()
            self.checkEnd()

    def checkEnd(self):
        return self.winner

    def __NextLevel(self):
        self.level += 1
        self.enemyVelocity *= 1.1  # enemies move 10% faster with every level, capping at 10 (25th level)
        self.__init__(self.queue, self.numOfPlayers, self.player1.name,
                      self.player2.name if self.numOfPlayers == 2 else "Player2",
                      self.level, self.player1.score,
                      self.player2.score if self.numOfPlayers == 2 else 0, self.enemyVelocity)
        self.start()
