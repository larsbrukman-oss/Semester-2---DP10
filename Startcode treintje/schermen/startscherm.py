from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

#regel 1 tm 3 importeren klasse die hier worden gebruikt om deze GUI te bouwen

class Startscherm(QWidget): # startscherm is een QWidget
    def __init__(self, main_window): 
        super().__init__() #roep de constructor van de superklasse (QWidget) aan
        self.main_window = main_window
        layout = QVBoxLayout() #Verticale layout wordt hiermee toegepast


        layout.setContentsMargins(40, 20, 40, 40)
        layout.setSpacing(20)
  
        label = QLabel('<span style="font-size:20pt">Welkom bij <b>Lake Side Mania</b>!</span>')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        label.setFont(QFont("Arial", 20))
    
        label.setStyleSheet(
            "QLabel{background-color: white; color: black; border: 1px solid black; border-radius: 18px; padding: 10px 18px;}"
        )
  
        btn_start = QPushButton("Volg de trein")
        btn_start.setFixedSize(200, 50)
        btn_start.clicked.connect(self.naar_volgende_scherm)
        # pil-vorm, groen, witte tekst
        btn_start.setStyleSheet(
            "QPushButton{background-color: #28a745; color: white; border-radius: 25px; font-weight: 600;}"
        )


        layout.addStretch(1)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch(2)
        layout.addWidget(btn_start, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch(3)

        self.setLayout(layout)

    def naar_volgende_scherm(self):
        self.main_window.toon_pagina(self.main_window.scherm2)
