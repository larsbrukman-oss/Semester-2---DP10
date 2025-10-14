from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy, QMessageBox
from PyQt6.QtCore import Qt
import random

# Import MapWidget from scherm2 so we reuse the exact same drawing logic.
from .scherm2 import MapWidget


class Scherm4(QWidget):
    """Full-window map view.

    This screen reuses the MapWidget from `scherm2` but expands it to take
    all available space. When the screen becomes visible we copy the
    current train position, attractions and platforms from `scherm2` so the
    view matches what the user was looking at.
    """

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)

        # Map should expand to take all available space
        self.map_widget = MapWidget()
        # Allow the map to expand to fill all available space.
        # PyQt6 uses the QSizePolicy.Policy enum for policy values.
        self.map_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.map_widget)
        # Connect train click signal to a handler that shows info.
        try:
            self.map_widget.train_clicked.connect(self._on_train_clicked)
            # Connect attraction clicks to show wait times
            try:
                self.map_widget.attraction_clicked.connect(self._on_attraction_clicked)
            except Exception:
                pass
        except Exception:
            pass

        # Bottom row with a single back button (or we could add controls here)
        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        self.btn_terug = QPushButton("Terug")
        self.btn_terug.setFixedSize(160, 44)
        # Match the green pill style used elsewhere
        self.btn_terug.setStyleSheet("QPushButton{background-color: #28a745; color: white; border-radius: 22px; font-weight: 600;}")
        self.btn_terug.clicked.connect(self.terug)
        btn_row.addWidget(self.btn_terug)
        btn_row.addStretch(1)
        layout.addLayout(btn_row)

        self.setLayout(layout)

    def showEvent(self, event):
        """When shown, sync data from scherm2 so the large map matches state."""
        try:
            s2 = getattr(self.main_window, 'scherm2', None)
            if s2:
                # copy train position
                if hasattr(s2, 'current_pos'):
                    self.map_widget.set_dot_normalized(*s2.current_pos)
                # copy attractions and platforms if present
                if hasattr(s2, 'attractions'):
                    self.map_widget.set_attractions(s2.attractions)
                if hasattr(s2, 'platforms'):
                    self.map_widget.set_platforms(s2.platforms)
                # copy train info if available
                if hasattr(s2, 'train_info'):
                    try:
                        self.map_widget.set_train_info(s2.train_info)
                    except Exception:
                        pass
                # If scherm2 exposes a train_updated signal, connect so we
                # receive live updates while this screen is visible.
                try:
                    s2.train_updated.connect(self._on_train_updated)
                except Exception:
                    pass
        except Exception:
            # Keep fail-safe: don't crash the whole app if something is missing.
            pass

        super().showEvent(event)

    def hideEvent(self, event):
        # Disconnect the live update signal to avoid duplicate connections.
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

    def _on_train_updated(self, info: dict, pos: tuple):
        """Receive live updates from scherm2 and refresh the fullscreen map."""
        try:
            # update position and stored info on the map widget
            if pos:
                self.map_widget.set_dot_normalized(*pos)
            if info:
                self.map_widget.set_train_info(info)
        except Exception:
            pass

    def terug(self):
        # Return to the previous screen (start from scherm2 for simplicity)
        try:
            self.main_window.toon_pagina(self.main_window.scherm2)
        except Exception:
            pass

    def _on_train_clicked(self, info: dict):
        """Show a small dialog with train information (seats and arrival)."""
        try:
            seats_available = int(info.get('seats_available', 0))
            total = int(info.get('total_seats', 20))
            minutes = info.get('arrival_minutes', None)
            dest = info.get('destination', None)
            reservations = int(info.get('reservations_for_destination', 0))

            text = f"Seats available: {seats_available} / {total}\n"
            if minutes is not None:
                text += f"Arrival: {minutes} minutes\n"
            else:
                text += "Arrival: unknown\n"
            if dest:
                text += f"Destination: {dest}\n"
                text += f"Reservations for destination: {reservations}\n"

            # Sanity statement: reserved + onboard must not exceed total seats.
            onboard = total - seats_available
            if onboard + reservations > total:
                text += "WARNING: reservations + onboard exceed train capacity!\n"
            else:
                text += "Reservation status: OK\n"

            dlg = QMessageBox(self)
            dlg.setWindowTitle('Trein informatie')
            dlg.setText(text)
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.exec()
        except Exception:
            pass

    def _on_attraction_clicked(self, label: str):
        """Show a small dialog with simulated wait times for the attraction."""
        try:
            waits = [random.randint(5, 45) for _ in range(3)]
            text = f"Wachttijden voor {label}:\n"
            for i, w in enumerate(waits, start=1):
                text += f"  Rij {i}: {w} min\n"

            dlg = QMessageBox(self)
            dlg.setWindowTitle(f"Wachttijden - {label}")
            dlg.setText(text)
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.exec()
        except Exception:
            pass
