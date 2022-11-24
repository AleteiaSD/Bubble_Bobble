from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QIcon, QFont, QPalette, QImage, QBrush
import sys
from multiprocessing import Queue
from game_logic.game import Game
from game_logic.TournamentWindow import TournamentWindow
from game_logic.MultiplayerWindow import MultiplayerWindow


class AnotherWindow(QWidget):
    """
    This window atm is not needed, l just added it for a test.
    I left it here if l ever need it in future.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setFixedSize(600, 600)
        self.setWindowTitle('BubbleBobble')
        self.setWindowIcon(QIcon('open.xpm'))
        self.setLayout(layout)


class Project(QWidget):

    def __init__(self):
        super().__init__()

        self.project_ui()

    def project_ui(self):
        weight = 500
        height = 500
        self.q = Queue()
        self.w = None
        self.name = ""
        image = QImage("resource/test.jpg")

        exitButton = QPushButton("EXIT", self)
        exitButton.clicked.connect(QCoreApplication.instance().quit)
        exitButton.setFixedSize(80, 35)

        playButton = QPushButton("1 PLAYER", self)
        playButton.setStyleSheet('QPushButton {background-color: #0041C2; color: white;}')
        playButton.setFont(QFont('Arial Black', 15))
        playButton.clicked.connect(self.show_1player_window)
        playButton.setFixedSize(120, 40)

        playButton2 = QPushButton("2 PLAYERS", self)
        playButton2.setStyleSheet('QPushButton {background-color: #0041C2; color: white;}')
        playButton2.setFont(QFont('Arial Black', 15))
        playButton2.clicked.connect(self.show_2players_window)
        playButton2.setFixedSize(130, 40)

        tournamentButton = QPushButton("TOURNAMENT", self)
        tournamentButton.setStyleSheet('QPushButton {background-color: #0041C2; color: white;}')
        tournamentButton.setFont(QFont('Arial Black', 10))
        tournamentButton.clicked.connect(self.show_tournament_window)
        tournamentButton.setFixedSize(130, 40)

        hbox = QHBoxLayout()
        hbox.addSpacing(2)
        hbox.setAlignment(Qt.AlignCenter)
        hbox.addWidget(playButton)
        hbox.addWidget(playButton2)
        hbox.addWidget(tournamentButton)

        connect_box = QVBoxLayout(self)
        connect_box.setAlignment(Qt.AlignCenter)
        connect_box.addLayout(hbox)
        connect_box.addWidget(exitButton, alignment=Qt.AlignCenter)

        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(image))

        self.setFixedSize(weight, height)
        self.setWindowTitle('BubbleBobble')
        self.setWindowIcon(QIcon('resource/player1.png'))

        self.setPalette(palette)

        self.show()

    def show_1player_window(self):
        self.w = Game(self.q, 1)
        self.w.start()

    def show_2players_window(self):
        self.w = MultiplayerWindow()

    def show_tournament_window(self):
        self.w = TournamentWindow()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pr = Project()
    sys.exit(app.exec_())
