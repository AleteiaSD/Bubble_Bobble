import sys
from multiprocessing import Queue, Process

from PyQt5.QtWidgets import QApplication
from game_logic.game import Game


class Multiplayer(Game):

    w = ""

    def __init__(self, queue: Queue, num, player1_input, player2_input, level=1, score1=0, score2=0, velocity=1):
        self.queue = queue
        super().__init__(queue, num, player1_input, player2_input, level, score1, score2, velocity)

    def readWinner(self):
        f = open('winner.txt', 'r')
        self.w = f.read()
        return self.w

    def checkEnd(self):
       self.queue.put(self.readWinner())
       self.queue.close()

def start_multiplayer_game(player1_input, player2_input):

    q = Queue()
    winner1_id = _start_game_process(q, player1_input, player2_input)
    print("Winner: ", winner1_id)


def _start_game_process(q, player1_input, player2_input) -> str:

    process = Process(target=_start_game, args=(q, player1_input, player2_input))
    process.start()

    winner_id = q.get()
    process.terminate()
    return winner_id

def _start_game(queue: Queue, player1_id,  player2_id):
    app = QApplication(sys.argv)
    game = Multiplayer(queue=queue, num=2, player1_input=player1_id, player2_input=player2_id)
    game.start()
    sys.exit(app.exec_())

