from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class Scherm3(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Dit is scherm 3"))

        # TODO: ervoor zorgen dat als je op een product klikt je naar het juiste product gaat
        btn_naar_scherm_4 = QPushButton("Naar scherm 4")
        btn_naar_scherm_4.clicked.connect(self.open_scherm)
        layout.addWidget(btn_naar_scherm_4)

        self.setLayout(layout)

    def open_scherm(self):
        self.main_window.toon_pagina(self.main_window.scherm4)
