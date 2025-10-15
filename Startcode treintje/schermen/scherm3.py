from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

class Scherm3(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        # Top row: terug knop linksboven
        top_row = QHBoxLayout()
        self.btn_terug = QPushButton("Terug")
        self.btn_terug.setFixedSize(120, 40)
        self.btn_terug.setStyleSheet("QPushButton{background-color: #28a745; color: white; border-radius: 20px; font-weight: 600;}")
        self.btn_terug.clicked.connect(lambda: self.main_window.toon_pagina(self.main_window.scherm2))
        top_row.addWidget(self.btn_terug)
        top_row.addStretch(1)
        layout.addLayout(top_row)

        layout.addWidget(QLabel("Dit is scherm 3"))

        # TODO: ervoor zorgen dat als je op een product klikt je naar het juiste product gaat
        btn_naar_scherm_4 = QPushButton("Naar scherm 4")
        btn_naar_scherm_4.clicked.connect(self.open_scherm)
        layout.addWidget(btn_naar_scherm_4)

        self.setLayout(layout)

    def open_scherm(self):
        self.main_window.toon_pagina(self.main_window.scherm4)
