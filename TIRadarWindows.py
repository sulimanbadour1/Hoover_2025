import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QTextEdit

class TIRadarWindow(QWidget):

    def __init__(self):
        super().__init__()

    def createGUI(self):
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")