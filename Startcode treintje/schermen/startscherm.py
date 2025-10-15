# Startscherm.py - GUI scherm met tekst en startknop
# Hier is het start scherm van de applicatie waarin je wordt verwelkomd en een knop hebt om naar het volgende scherm te gaan.


# Hier worden de benodigde klassen uit PyQt6 geïmporteerd

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton #Widgets en layout klassen
from PyQt6.QtCore import Qt                                           
from PyQt6.QtGui import QFont                                         #Lettertype en stijl klassen

# Klasse : Startscherm
# Dit is de klasse die eerste scherm van de applicatie voorstelt,
# Deze klasse erft van QWidget en dat betekent dat het een venster is dat kan worden weergegeven in de GUI.

class Startscherm(QWidget):
    def __init__(self, main_window): 
        super().__init__() 
        self.main_window = main_window
        layout = QVBoxLayout() 


# Hier stellen we de marges en tussenruimte tussen de widgets in

        layout.setContentsMargins(40, 20, 40, 40)
        layout.setSpacing(20)

# Hier wordt het welkomstbericht en de startknop gemaakt en gestyled
# <b> en <span> zijn HTML-tags die wij gebruiken om de tekst hier te stylen
# we bepalen hier eigenlijk de stijl van de tekst en knop

        label = QLabel('<span style="font-size:20pt">Welkom bij <b>Lake Side Mania</b>!</span>') 
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        label.setFont(QFont("Arial", 20))
    
        label.setStyleSheet(
            "QLabel{background-color: white; color: black; border: 1px solid black; border-radius: 18px; padding: 10px 18px;}"
        ) 

# Hier wordt de startknop gemaakt en gestyled en hiermee ga je naar het volgende scherm
        btn_start = QPushButton("Volg de trein")
        btn_start.setFixedSize(200, 50)
        btn_start.clicked.connect(self.naar_volgende_scherm)
        btn_start.setStyleSheet(
            "QPushButton{background-color: #28a745; color: white; border-radius: 25px; font-weight: 600;}"
        )

# de addStretch wordt gebruikt om ruimte toe te voegen tussen de widgets

        layout.addStretch(1)
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch(2)
        layout.addWidget(btn_start, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch(3)

        self.setLayout(layout)

# Functie (Volgende scherm)
# Deze functie gebruiken wij om naar het volgende scherm te gaan als de startknop wordt ingedrukt
# specifiek scherm2 wordt hier aangeroepen

    def naar_volgende_scherm(self):
        self.main_window.toon_pagina(self.main_window.scherm2)
