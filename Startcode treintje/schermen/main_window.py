from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QPushButton
from .startscherm import Startscherm
from .scherm3 import Scherm3
from .scherm2 import Scherm2
from .scherm4 import Scherm4
from .scherm1 import Scherm1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lake Side Mania - GUI")
        self.setGeometry(100, 100, 1024, 768)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Pagina's
        self.startscherm = Startscherm(self)
        self.scherm1 = Scherm1(self)
        self.scherm2 = Scherm2(self)
        self.scherm3 = Scherm3(self)  
        self.scherm4 = Scherm4(self)  
       
        # Voeg toe aan stack
        self.stack.addWidget(self.startscherm)
        self.stack.addWidget(self.scherm3)
        self.stack.addWidget(self.scherm2)
        self.stack.addWidget(self.scherm4)
        self.stack.addWidget(self.scherm1)

        self.stack.setCurrentWidget(self.startscherm)

    def toon_pagina(self, widget: QWidget):
        self.stack.setCurrentWidget(widget)
