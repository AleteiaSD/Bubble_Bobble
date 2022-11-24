import sys
from threading import Thread

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QComboBox, QMessageBox, QVBoxLayout
from game_logic.Tournament import start_tournament

class TournamentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setFixedSize(500, 500)
        self.setWindowTitle("Tournament")
        self.setLayout(layout)
        self.winner = None
        self.initUI()


    def initUI(self):
        self.initWindow()
        self.username()
        self.labels()
        self.buttonPlay()
        self.show()


    def initWindow(self):
        self.BackGround = QPixmap("resource/image.jpg")
        self.BackGroundLabel = QtWidgets.QLabel(self)
        self.BackGroundLabel.setPixmap(self.BackGround)
        self.BackGroundLabel.setGeometry(0, 0, 500, 500)

    def username(self):
        self.lbl2 = QtWidgets.QLabel(self)
        self.lbl2.setText("Enter name")
        self.lbl2.setGeometry(250, 30, 200, 60)
        self.lbl2.setStyleSheet(" color: rgb(64, 39, 36);font-size: 16px; font-family: Arial Black;")

        self.player1NameLineEdit = QLineEdit(self)
        self.player1NameLineEdit.setGeometry(200, 100, 200, 40)
        self.player2NameLineEdit = QLineEdit(self)
        self.player2NameLineEdit.setGeometry(200, 200, 200, 40)
        self.player3NameLineEdit = QLineEdit(self)
        self.player3NameLineEdit.setGeometry(200, 300, 200, 40)
        self.player4NameLineEdit = QLineEdit(self)
        self.player4NameLineEdit.setGeometry(200, 400, 200, 40)



    def labels(self):
        self.lbl3 = QtWidgets.QLabel(self)
        self.lbl3.setText("First player")
        self.lbl3.setGeometry(50, 100, 200, 40)
        self.lbl3.setStyleSheet("color: rgb(64, 39, 36); font-size: 16px; font-family: Arial Black;")

        self.lbl4 = QtWidgets.QLabel(self)
        self.lbl4.setText("Second player")
        self.lbl4.setGeometry(50, 200, 200, 40)
        self.lbl4.setStyleSheet("color: rgb(64, 39, 36);font-size: 16px; font-family: Arial Black;")

        self.lbl5 = QtWidgets.QLabel(self)
        self.lbl5.setText("Third player")
        self.lbl5.setGeometry(50, 300, 200, 40)
        self.lbl5.setStyleSheet(" color: rgb(64, 39, 36);font-size: 16px; font-family: Arial Black;")

        self.lbl6 = QtWidgets.QLabel(self)
        self.lbl6.setText("Fourth player")
        self.lbl6.setGeometry(50, 400, 200, 40)
        self.lbl6.setStyleSheet("color: rgb(64, 39, 36);font-size: 16px; font-family: Arial Black;")

    def buttonPlay(self):
        self.playButton = QtWidgets.QPushButton(self)
        self.playButton.setText("PLAY")
        self.playButton.setGeometry(200, 450, 200, 40)
        self.playButton.setStyleSheet(
            "border:2px solid rgb(64, 39, 36); color: rgb(64, 39, 36); font-size: 26px; font-family: Arial Black;")
        self.playButton.clicked.connect(self.onPlayButtonClicked)

    def onPlayButtonClicked(self):
        if self.player1NameLineEdit.text() == "" or self.player2NameLineEdit.text() == "" \
                or self.player3NameLineEdit.text() == "" or self.player4NameLineEdit.text() == "" :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.NoIcon)
            msg.setText("Enter your username")
            msg.setWindowTitle("Error")
            msg.exec_()

        elif self.player1NameLineEdit.text() == self.player2NameLineEdit.text() \
                or self.player1NameLineEdit.text() == self.player3NameLineEdit.text() \
                or self.player1NameLineEdit.text() == self.player4NameLineEdit.text() \
                or self.player2NameLineEdit.text() == self.player3NameLineEdit.text() \
                or self.player2NameLineEdit.text() == self.player4NameLineEdit.text() \
                or self.player3NameLineEdit.text() == self.player4NameLineEdit.text():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.NoIcon)
            msg.setText("Username must be unique")
            msg.setWindowTitle("Error")
            msg.exec_()

        else:
            player1_input = self.player1NameLineEdit.text()
            player2_input = self.player2NameLineEdit.text()
            player3_input = self.player3NameLineEdit.text()
            player4_input = self.player4NameLineEdit.text()


            #start_tournament(player1_input, player2_input, player3_input, player4_input)
            thread = Thread(target=start_tournament, args=(player1_input, player2_input, player3_input, player4_input))
            thread.daemon = True
            thread.start()
            self.hide()
            self.player1NameLineEdit.setText("")
            self.player2NameLineEdit.setText("")
            self.player3NameLineEdit.setText("")
            self.player4NameLineEdit.setText("")

