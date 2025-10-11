from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class Scherm4(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Dit is scherm 4"))

        btn_naar_scherm_1 = QPushButton("Naar scherm 1")
        btn_naar_scherm_1.clicked.connect(self.open_scherm)
        layout.addWidget(btn_naar_scherm_1)

        self.setLayout(layout)

    def open_scherm(self):
        self.main_window.toon_pagina(self.main_window.scherm1)
