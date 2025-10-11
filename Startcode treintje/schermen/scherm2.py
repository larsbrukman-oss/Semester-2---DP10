from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class Scherm2(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Dit is scherm 2"))

        # TODO: wellicht kunnen jullie vanuit meerdere pagina's de winkelmand openen. 
        # Gedeelde functionaliteit hoe los je dat met OOP op?
        btn_naar_scherm3 = QPushButton("Naar scherm 3")
        btn_naar_scherm3.clicked.connect(self.open_scherm)
        layout.addWidget(btn_naar_scherm3)

        # TODO: Je kunt vanuit hier naar de winkelmand pagina, maar hoe krijg je een product in de winkelmand?

        self.setLayout(layout)

    def open_scherm(self):
        self.main_window.toon_pagina(self.main_window.scherm3)
