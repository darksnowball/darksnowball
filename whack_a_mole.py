import sys
import random
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QInputDialog, QMessageBox
from PyQt5.QtGui import QColor, QFont

class WhackAMoleGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Prompt user for game duration (between 15 and 60 seconds)
        self.duration, ok = QInputDialog.getInt(self, "Game Duration", "Enter duration (15-60 seconds):", 30, 15, 60, 1)
        if not ok:
            sys.exit()  # Exit if the user cancels the input dialog

        self.setWindowTitle("Whack-a-Mole")
        self.setGeometry(100, 100, 400, 400)
        self.score = 0
        self.grid_size = 3  # 3x3 grid

        # Layouts
        self.layout = QVBoxLayout()
        self.score_label = QLabel(f"Score: {self.score}")
        self.score_label.setFont(QFont('Arial', 16))
        self.layout.addWidget(self.score_label)

        # Create grid layout for moles
        self.grid_layout = QGridLayout()
        self.buttons = [[QPushButton('') for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j].setFixedSize(100, 100)  # Button size
                self.buttons[i][j].setStyleSheet('background-color: lightgray;')  # Default button color
                self.buttons[i][j].clicked.connect(self.handle_click(i, j))
                self.grid_layout.addWidget(self.buttons[i][j], i, j)
        self.layout.addLayout(self.grid_layout)

        self.setLayout(self.layout)

        # Start the mole movement timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_mole_position)
        self.timer.start(1000)  # Mole moves every second

        # Set game end time
        self.end_time = QTime.currentTime().addSecs(self.duration)
        self.end_timer = QTimer(self)
        self.end_timer.timeout.connect(self.check_end_time)
        self.end_timer.start(1000)

        self.update_mole_position()

    def handle_click(self, i, j):
        def click_event():
            if self.buttons[i][j].text() == 'Mole':
                self.score += 1
                self.score_label.setText(f"Score: {self.score}")
                self.buttons[i][j].setStyleSheet('background-color: lightgray;')  # Reset color after click
                self.buttons[i][j].setText('')  # Clear the mole text
                self.update_mole_position()  # Move the mole
        return click_event

    def update_mole_position(self):
        # Clear all buttons first
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j].setText('')
                self.buttons[i][j].setStyleSheet('background-color: lightgray;')

        # Randomly place a mole on the grid
        mole_i = random.randint(0, self.grid_size - 1)
        mole_j = random.randint(0, self.grid_size - 1)
        self.buttons[mole_i][mole_j].setText('Mole')
        self.buttons[mole_i][mole_j].setStyleSheet('background-color: green; color: white; font-weight: bold;')  # Mole color

    def check_end_time(self):
        if QTime.currentTime() >= self.end_time:
            self.end_game()





    def end_game(self):
        self.timer.stop()
        self.end_timer.stop()
        self.save_score()
        QMessageBox.information(self, "Game Over", f"Time's up! Your final score is: {self.score}")
        self.close()

    def save_score(self):
        with open('score.txt', 'a') as f:
            f.write(f"Score: {self.score}\n")
        print("Game over. Your score has been saved.")

def main():
    app = QApplication(sys.argv)
    game = WhackAMoleGame()
    game.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    