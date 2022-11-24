from PyQt5 import QtCore


BLOCK_SIZE = 40
WIDTH = 800
HEIGHT = 680
winner = ""
COLORS = ['#d5ddf3', '#f3d5dd']
RANDOM_BUFF_POINTS = ['POINTS_UP', 'POINTS_DOWN']
RANDOM_BUFF_LIVES = ['LIVES_UP', 'LIVES_DOWN']
RANDOM_BUFF_TYPE = ['LIVES', 'POINTS']

STRONG_ENEMY_LEVEL_REQUIREMENT = 1  # after the 3rd level, stronger enemies will occur

# in seconds
PLAYER_MOVEMENT_PERIOD = 0.05
ENEMY_MOVEMENT_PERIOD = 0.01
BUBBLE_MOVEMENT_PERIOD = 0.01
BUFF_CHECK_PERIOD = 0.01
GRAVITY_CHECK_PERIOD = 0.02
JUMP_CHECK_PERIOD = 0.06
BUBBLE_CREATION_PERIOD = 0.5
IMMUNE_PERIOD = 3
BUFF_SPAWN_PERIOD = [15, 40]

KeyMappingPlayer1 = {
    QtCore.Qt.Key_W: 'UP',
   # QtCore.Qt.Key_S: 'DOWN', umesto ovoga ide gravitacija
    QtCore.Qt.Key_D: 'RIGHT',
    QtCore.Qt.Key_A: 'LEFT',
    QtCore.Qt.Key_Space: 'SHOOT'
}

KeyMappingPlayer2 = {
    QtCore.Qt.Key_Up: 'UP',
   # QtCore.Qt.Key_Down: 'DOWN', umesto ovoga ide gravitacija
    QtCore.Qt.Key_Right: 'RIGHT',
    QtCore.Qt.Key_Left: 'LEFT',
    QtCore.Qt.Key_P: 'SHOOT'
}

Moves = {
    'UP': (0, -BLOCK_SIZE // 2),
    'DOWN': (0, BLOCK_SIZE // 2),
    'LEFT': (-BLOCK_SIZE // 2, 0),
    'RIGHT': (BLOCK_SIZE // 2, 0)
}

MappingPicturesOfEnemiesAndBalloons = {
    ('resource/balloon1.png', 'resource/enemy1.png'): 'resource/e1b1.png',
    ('resource/balloon1.png', 'resource/enemy2.png'): 'resource/e2b1.png',
    ('resource/balloon1.png', 'resource/simple_enemy1.png'): 'resource/se1b1.png',
    ('resource/balloon1.png', 'resource/simple_enemy2.png'): 'resource/se2b1.png',
    ('resource/balloon2.png', 'resource/enemy1.png'): 'resource/e1b2.png',
    ('resource/balloon2.png', 'resource/enemy2.png'): 'resource/e2b2.png',
    ('resource/balloon2.png', 'resource/simple_enemy1.png'): 'resource/se1b2.png',
    ('resource/balloon2.png', 'resource/simple_enemy2.png'): 'resource/se2b2.png'

}
