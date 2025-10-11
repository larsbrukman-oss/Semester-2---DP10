from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class Startscherm(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Welkom bij Lake Side Mania!"))

        btn_start = QPushButton("Tik om te starten!")
        btn_start.clicked.connect(self.naar_volgende_scherm)
        layout.addWidget(btn_start)

        self.setLayout(layout)

    def naar_volgende_scherm(self):
        self.main_window.toon_pagina(self.main_window.scherm2)
