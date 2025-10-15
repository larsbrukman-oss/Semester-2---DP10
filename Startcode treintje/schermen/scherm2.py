# Scherm2.py - Tweede scherm van de applicatie met een kaart en knoppen
# Dit scherm toont een interactieve kaart en de mogelijkheid om diverse handelingen uit te voeren.

# Hier worden de benodigde klassen uit PyQt6 geïmporteerd
# We importeren hier ook "import random" omdat we willekeurige posities willen genereren voor de locatie van de trein

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QBrush, QColor
import random

# Klasse : Scherm 2
# Deze klasse is het 2e scherm van de applicatie, waar de gebruiker een kaart ziet met daarop de locatie van een treintje. 
# deze klasse bevatt ook knoppen om de locatie te verversen, te vergroten en iets te reserveren.

class Scherm2(QWidget):
    train_updated = pyqtSignal(dict, tuple)        # Info over de trein

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

# Deze "terug" knop brengt je terug naar het startscherm

        top_row = QHBoxLayout()
        self.btn_terug_top = QPushButton("Terug")
        self.btn_terug_top.setFixedSize(120, 40)
        self.btn_terug_top.setStyleSheet("QPushButton{background-color: #28a745; color: white; border-radius: 20px; font-weight: 600;}")

# Hier kan je dmv een klik terug naar het startscherm

        self.btn_terug_top.clicked.connect(lambda: self.main_window.toon_pagina(self.main_window.startscherm))
        top_row.addWidget(self.btn_terug_top)      # Voeg de terug knop toe : linksboven
        top_row.addStretch(1)
        layout.addLayout(top_row)

        layout.addStretch(1)

# Kaart widget in het midden van het scherm

        self.map_container = QHBoxLayout()
        self.map_container.addStretch(1)
        self.map_widget = MapWidget()
        self.map_container.addWidget(self.map_widget)
        self.map_container.addStretch(1)
        layout.addLayout(self.map_container)

# Attracties: punten op de kaart.

        self.attractions = [
            (0.2, 0.2, "Rollercoaster"),
            (0.8, 0.25, "Ferris Wheel"),
            (0.5, 0.7, "Haunted House"),
        ]
        self.map_widget.set_attractions(self.attractions)

# Perrons: punten op de kaart.

        self.platforms = [
            (0.12, 0.86, "Perron 1"),
            (0.88, 0.86, "Perron 2"),
        ]

# Hier maken we een dict aan om reserveringen bij te houden voor elk perron.

        self.map_widget.set_platforms(self.platforms)
        self.reservations = {label: 0 for (_, _, label) in self.platforms}

        layout.addSpacing(12)

# Middenrij: twee belangrijke acties naast elkaar onder de kaart.

        middle_row = QHBoxLayout()
        middle_row.addStretch(1)

# Actie (knop) 1 : "Volg de trein" - ververst de locatie van de trein op de kaart.

        btn_ververs = QPushButton("Volg de trein")
        btn_ververs.setFixedSize(200, 50)
        btn_ververs.clicked.connect(self.ververs_locatie)    # Hier wordt de klikactie gekoppeld aan de functie ververs_locatie
        btn_ververs.setStyleSheet(
            "QPushButton{background-color: #28a745; color: white; border-radius: 25px; font-weight: 600;}"
        )
        middle_row.addWidget(btn_ververs)

        middle_row.addSpacing(12)

# Actie (knop) 2 : "Vergroot" - vergroot de kaartweergave (Dit navigeert naar scherm4).

        self.vergroot_btn = QPushButton("Vergroot")
        self.vergroot_btn.setFixedSize(200, 50)
        self.vergroot_btn.clicked.connect(self.open_scherm4) # Hier wordt de klikactie gekoppeld aan de functie open_scherm4
        self.vergroot_btn.setStyleSheet("QPushButton{background-color: #0069d9; color: white; border-radius: 25px;}" )
        middle_row.addWidget(self.vergroot_btn)

        middle_row.addStretch(1)
        layout.addLayout(middle_row)

        layout.addStretch(1)

# Actie (knop) 3 : een Reserveer knop.

        lower_row = QHBoxLayout()
        lower_row.addStretch(1)
        btn_reserveer = QPushButton("Reserveer")
        btn_reserveer.setFixedSize(200, 50)
        btn_reserveer.clicked.connect(self.open_scherm3)    # Hier wordt de klikactie gekoppeld aan de functie open_scherm3 
        btn_reserveer.setStyleSheet(
            "QPushButton{background-color: #28a745; color: white; border-radius: 25px; font-weight: 600;}"
        )
        lower_row.addWidget(btn_reserveer)
        lower_row.addStretch(1)
        layout.addLayout(lower_row)

        self.setLayout(layout)

# start locatie van de trein 

        self.current_pos = (0.5, 0.5)
        self.map_widget.set_dot_normalized(*self.current_pos)
        
#informatie over de trein

        self.train_info = {"seats_available": 20, "total_seats": 20, "arrival_minutes": 0}

    def get_train_info(self):
        return getattr(self, 'train_info', {"seats_available": 0, "total_seats": 20, "arrival_minutes": 0})

    def resizeEvent(self, event):
        try:
            h = max(220, int(self.main_window.size().height() * 0.55))
        except Exception:
            h = max(220, int(self.size().height() * 0.55))

        self.map_widget.setFixedSize(h, h)
        super().resizeEvent(event)

    def position_vergroot_button(self):
        return

# Hier verversen we de locatie van de trein op de kaart met willekeurige coördinaten

    def ververs_locatie(self):
        x = random.random()
        y = random.random()
        self.current_pos = (x, y)
        self.map_widget.set_dot_normalized(x, y)

# Hier genereren we willekeurige info over de trein

        seats = random.randint(0, 20)
        minutes = random.randint(1, 12)
        dest_label = None
        reservations_for_dest = 0

# Hier kiezen we een willekeurige bestemming en bepalen we het aantal reserveringen

        try:
            if self.platforms :
                dest_label = random.choice(self.platforms)[2]
                proposed = random.randint(0, 15)
                onboard = 20 - seats
                max_allowed_reservations = max(0, 20 - onboard)
                reservations_for_dest = min(proposed, max_allowed_reservations)
                self.reservations[dest_label] = reservations_for_dest
        except Exception:
            dest_label = None

# Update de trein info en kaartweergave

        self.train_info = {
            "seats_available": seats,
            "total_seats": 20,
            "arrival_minutes": minutes,
            "destination": dest_label,
            "reservations_for_destination": reservations_for_dest,
        }
        try:
            self.map_widget.set_train_info(self.train_info)
        except Exception:
            pass
        try:
            self.train_updated.emit(self.train_info, self.current_pos)
        except Exception:
            pass

# Hiermee ga je naar scherm4 (vergroot scherm)

    def open_scherm4(self):
        if (self, 'main_window') and self.main_window:
            try:
                self.main_window.toon_pagina(self.main_window.scherm4)
            except Exception:
                pass

# Hiermee ga je naar scherm3 (reserveren)

    def open_scherm3(self):
        if (self, 'main_window') and self.main_window:
            try:
                self.main_window.toon_pagina(self.main_window.scherm3)
            except Exception:
                pass

# Klasse : interactieve MapWidget
# Deze klasse tekent een kaart met de trein, attracties en perrons.
# De kaart reageert op muisklikken om informatie over de trein of attracties te tonen.

class MapWidget(QWidget):
    train_clicked = pyqtSignal(dict)
    attraction_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dot = (0.5, 0.5)
        self.setMinimumSize(220, 220)
        self._train_info = {"seats_available": 20, "total_seats": 20, "arrival_minutes": 0}

# hier wordt de positie van de trein ingesteld / geupdate

    def set_dot_normalized(self, x, y):
        x = min(max(0.0, float(x)), 1.0)
        y = min(max(0.0, float(y)), 1.0)
        self._dot = (x, y)
        self.update()

    def set_attractions(self, attractions):
        self._attractions = attractions
        self.update()

# hier wordt de info van de trein geupdate

    def set_train_info(self, info: dict):
        self._train_info = dict(info) if info is not None else {}
        self.update()

    def set_platforms(self, platforms):
        self._platforms = platforms
        self.update()

# Tekent de achtergrond, kaart, de trein, attracties en perrons.

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(230, 230, 230)))
        pen = painter.pen()
        pen.setColor(QColor(160, 160, 160))
        pen.setWidth(4)
        painter.setPen(pen)
        painter.drawRect(self.rect())

        grid_pen = painter.pen()
        grid_pen.setColor(QColor(210, 210, 210))
        grid_pen.setWidth(1)
        painter.setPen(grid_pen)
        w = self.width()
        h = self.height()
        for i in range(1, 4):
            painter.drawLine(int(w * i / 4), 0, int(w * i / 4), h)
            painter.drawLine(0, int(h * i / 4), w, int(h * i / 4))

        dot_x = int(self._dot[0] * w)
        dot_y = int(self._dot[1] * h)
        radius = max(10, int(min(w, h) * 0.045))
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.setPen(Qt.GlobalColor.black)
        painter.drawEllipse(dot_x - radius, dot_y - radius, radius * 2, radius * 2)

        self._last_dot_rect = (dot_x - radius, dot_y - radius, radius * 2, radius * 2)

        self._last_attraction_positions = []
        if (self, '_attractions') and self._attractions:
            marker_radius = max(6, int(min(w, h) * 0.03))
            painter.setBrush(QBrush(QColor(200, 30, 30)))
            painter.setPen(Qt.GlobalColor.black)
            for (ax, ay, label) in self._attractions:
                mx = int(ax * w)
                my = int(ay * h)
                painter.drawEllipse(mx - marker_radius, my - marker_radius, marker_radius * 2, marker_radius * 2)
                painter.drawText(mx + marker_radius + 4, my + marker_radius // 2, label)
                self._last_attraction_positions.append((mx, my, marker_radius, label))

        if (self, '_platforms') and self._platforms:
            platform_marker_radius = max(6, int(min(w, h) * 0.03))
            painter.setBrush(QBrush(QColor(50, 120, 220)))
            painter.setPen(Qt.GlobalColor.black)
            for (px, py, plabel) in self._platforms:
                mx = int(px * w)
                my = int(py * h)
                painter.drawEllipse(mx - platform_marker_radius, my - platform_marker_radius, platform_marker_radius * 2, platform_marker_radius * 2)
                painter.drawText(mx + platform_marker_radius + 4, my + platform_marker_radius // 2, plabel)

# Hiermee kunnen muisklikken op de kaart worden verwerkt

    def mousePressEvent(self, event):
        try:
            x = event.position().x()
            y = event.position().y()
        except Exception:
            x = event.x()
            y = event.y()

# Hiermee kunnen we klik acties op de trein detecteren

        if (self, '_last_dot_rect'):
            rx, ry, rw, rh = self._last_dot_rect
            if rx <= x <= rx + rw and ry <= y <= ry + rh:
                try:
                    self.train_clicked.emit(getattr(self, '_train_info', {}))
                except Exception:
                    pass
                return

# Hiermee kunnen we klik acties op de attracties detecteren

        try:
            if (self, '_last_attraction_positions'):
                for (cx, cy, r, label) in self._last_attraction_positions:
                    dx = x - cx
                    dy = y - cy
                    if dx * dx + dy * dy <= r * r:
                        try:
                            self.attraction_clicked.emit(label)
                        except Exception:
                            pass
                        return
        except Exception:
            pass
        super().mousePressEvent(event)

    
