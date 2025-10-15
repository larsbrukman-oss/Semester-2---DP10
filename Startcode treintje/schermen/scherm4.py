from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy, QMessageBox
from PyQt6.QtCore import Qt
import random

from .scherm2 import MapWidget

# Klasse : Scherm4
# Dit is de klasse waarin de vergrote versie van de map wordt weergegeven

class Scherm4(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)

        
        self.map_widget = MapWidget()

        self.map_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.map_widget)
        # verbind signalen van de map widget
        try:
            self.map_widget.train_clicked.connect(self._on_train_clicked)
        except Exception:
            # als het signaal niet bestaat, negeren we het
            pass
        try:
            self.map_widget.attraction_clicked.connect(self._on_attraction_clicked)
        except Exception:
            pass

# Terug knop onderaan de pagina

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        self.btn_terug = QPushButton("Terug")
        self.btn_terug.setFixedSize(160, 44)
        self.btn_terug.setStyleSheet("QPushButton{background-color: #28a745; color: white; border-radius: 22px; font-weight: 600;}")
        self.btn_terug.clicked.connect(self.terug)
        btn_row.addWidget(self.btn_terug)
        btn_row.addStretch(1)
        layout.addLayout(btn_row)

#Dictionaries voor simulatie van wachttijden etz

        self.setLayout(layout)
        # Nederlandse namen voor simulatie-dictionaries
        self._wachttijden_attracties = {}
        self._extra_tijden_perron = {}
        self._aankomst_minuten_perron = {}
    
# Event bij het tonen van het scherm : Hierbij worden de gegevens van scherm2 opgehaald en weergegeven op de map

    def showEvent(self, event):
        
        try:
            s2 = getattr(self.main_window, 'scherm2', None)
            if s2:
                if hasattr(s2, 'current_pos'):
                    self.map_widget.set_dot_normalized(*s2.current_pos)
                if hasattr(s2, 'attractions'):
                    self.map_widget.set_attractions(s2.attractions)
                    for (_ax, _ay, label) in s2.attractions:
                        if label not in self._wachttijden_attracties:
                            self._wachttijden_attracties[label] = random.randint(3, 25)
                if hasattr(s2, 'platforms'):
                    self.map_widget.set_platforms(s2.platforms)
                if hasattr(s2, 'train_info'):
                    try:
                        self.map_widget.set_train_info(s2.train_info)
                    except Exception:
                        pass
                # connect signaal voor position updates als aanwezig
                try:
                    s2.train_updated.connect(self._on_train_updated)
                except Exception:
                    pass
        except Exception:
            pass

        super().showEvent(event)

# Event bij het verbergen van het scherm : Hierbij wordt de verbinding met scherm2 verbroken

    def hideEvent(self, event):
        
        try:
            s2 = getattr(self.main_window, 'scherm2', None)
            if s2:
                try:
                    s2.train_updated.disconnect(self._on_train_updated)
                except Exception:
                    pass
        except Exception:
            pass
        super().hideEvent(event)

# Event bij het updaten van de trein positie : Hierbij worden de gegevens van de trein bijgewerkt op de map

    def _on_train_updated(self, info: dict, pos: tuple):
        try:
            if pos:
                self.map_widget.set_dot_normalized(*pos)
            if info:
                self.map_widget.set_train_info(info)
        except Exception:
            pass

# Functie (Terug knop)
# Deze functie gebruiken wij om terug te gaan naar het vorige scherm (scherm2) als de terug knop wordt ingedrukt

    def terug(self):
        try:
            self.main_window.toon_pagina(self.main_window.scherm2)
        except Exception:
            pass

# toont informatie bij het klikken op de trein

    def _on_train_clicked(self, info: dict):
        try:
            seats_available = random.randint(0, 20)    
            total = 20

            platform_label = None
            platform_display = "-"
            reservations_for_platform = None
            try:
                s2 = getattr(self.main_window, 'scherm2', None)
                if s2 and hasattr(s2, 'platforms') and s2.platforms:
                    p = random.choice(s2.platforms)
                    platform_label = p[2]
                    platform_display = platform_label
                    try:
                        reservations_map = getattr(s2, 'reservations', {})
                        existing = int(reservations_map.get(platform_label, 0))
                        onboard = total - seats_available
                        max_allowed = max(0, total - onboard)
                        reservations_for_platform = max(0, max_allowed - existing)
                    except Exception:
                        reservations_for_platform = None
                else:
                    platform_display = f"Perron {random.randint(1,4)}"
            except Exception:
                platform_display = f"Perron {random.randint(1,4)}"

            text = f"plekken beschikbaar : {seats_available} / {total}\n"
            key_for_arrival = platform_label if platform_label else platform_display
            if key_for_arrival not in self._aankomst_minuten_perron:
                self._aankomst_minuten_perron[key_for_arrival] = random.randint(1, 12)
            arrival_min = self._aankomst_minuten_perron[key_for_arrival]
            text += f"aankomst tot {platform_display}: {arrival_min} minuten\n"
            show_extra = False
            try:
                if platform_label and ('2' in platform_label or platform_label.lower().strip() == 'perron 2'):
                    show_extra = True
                elif isinstance(platform_display, str) and '2' in platform_display:
                    show_extra = True
            except Exception:
                show_extra = False

            if reservations_for_platform is None:
                demo_reserve_spots = random.randint(0, max(0, total - (total - seats_available)))
                text += f"beschikbare plekken voor reservering: {demo_reserve_spots}\n"
            else:
                text += f"beschikbare plekken voor reservering: {reservations_for_platform}\n"

            dlg = QMessageBox(self)
            dlg.setWindowTitle('Trein informatie')
            dlg.setText(text)
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.exec()
        except Exception:
            pass

# Dit toont informatie bij het klikken op een attractie (specifiek de wachttijd)

    def _on_attraction_clicked(self, label: str):
        try:
            if label not in self._wachttijden_attracties:
                self._wachttijden_attracties[label] = random.randint(3, 25)
            wait = self._wachttijden_attracties[label]
            text = f"Wachttijd = {wait} minuut"

            dlg = QMessageBox(self)
            dlg.setWindowTitle(f"Wachttijd - {label}")
            dlg.setText(text)
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.exec()
        except Exception:
            pass
