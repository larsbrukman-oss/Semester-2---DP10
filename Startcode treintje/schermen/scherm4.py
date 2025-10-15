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
        # mapping from attraction label -> persistent wait time in minutes
        self._attraction_waits = {}
        # mapping from platform label -> persistent extra time (minutes)
        self._platform_extra_times = {}
        # mapping from platform label -> persistent arrival minutes shown after the platform
        self._platform_arrival_minutes = {}

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
                    # Ensure each attraction has a single persistent wait time.
                    # If we already generated a wait for a label, keep it.
                    for (_ax, _ay, label) in s2.attractions:
                        if label not in self._attraction_waits:
                            # random wait between 3 and 25 minutes
                            self._attraction_waits[label] = random.randint(3, 25)
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
        """Toont een compacte Nederlandse samenvatting wanneer de treindot wordt aangeklikt.

        We genereren voor de demo een willekeurig aantal beschikbare plekken
        (0..20). De aankomst wordt gekoppeld aan een willekeurig perron uit de
        lijst van `scherm2.platforms` (als die beschikbaar is), en we tonen
        hoeveel plekken er beschikbaar zijn voor reservering op dat perron
        op basis van `scherm2.reservations` als die aanwezig is.
        """
        try:
            # Seats available is randomized here for demo purposes.
            seats_available = random.randint(0, 20)
            total = 20

            # Choose a random platform (destination) if scherm2 exposes platforms
            platform_label = None
            platform_display = "-"
            reservations_for_platform = None
            try:
                s2 = getattr(self.main_window, 'scherm2', None)
                if s2 and hasattr(s2, 'platforms') and s2.platforms:
                    # pick a random platform tuple (x,y,label)
                    p = random.choice(s2.platforms)
                    platform_label = p[2]
                    platform_display = platform_label
                    # If reservations mapping exists, use it to compute available
                    # spots for reservation (total seats - onboard - existing reservations)
                    try:
                        reservations_map = getattr(s2, 'reservations', {})
                        existing = int(reservations_map.get(platform_label, 0))
                        onboard = total - seats_available
                        # maximum that can be reserved safely
                        max_allowed = max(0, total - onboard)
                        # available spots for reservation is what's left from max_allowed
                        reservations_for_platform = max(0, max_allowed - existing)
                    except Exception:
                        reservations_for_platform = None
                else:
                    # No platforms known; pick a synthetic label
                    platform_display = f"Perron {random.randint(1,4)}"
            except Exception:
                platform_display = f"Perron {random.randint(1,4)}"

            # Build the Dutch text lines requested by the user.
            text = f"plekken beschikbaar : {seats_available} / {total}\n"
            # Ensure we have a persistent arrival minute value per platform
            key_for_arrival = platform_label if platform_label else platform_display
            if key_for_arrival not in self._platform_arrival_minutes:
                self._platform_arrival_minutes[key_for_arrival] = random.randint(1, 12)
            arrival_min = self._platform_arrival_minutes[key_for_arrival]
            text += f"aankomst tot {platform_display}: {arrival_min} minuten\n"
            # If the chosen platform is Perron 2, show an extra persistent time
            show_extra = False
            try:
                if platform_label and ('2' in platform_label or platform_label.lower().strip() == 'perron 2'):
                    show_extra = True
                elif isinstance(platform_display, str) and '2' in platform_display:
                    show_extra = True
            except Exception:
                show_extra = False

            if show_extra:
                # ensure a persistent extra time for this platform label (or display)
                key = platform_label if platform_label else platform_display
                if key not in self._platform_extra_times:
                    self._platform_extra_times[key] = random.randint(1, 12)
                extra = self._platform_extra_times[key]
                text += f"extra verwerkingstijd: {extra} minuten\n"
            if reservations_for_platform is None:
                # If we couldn't compute real reservation capacity, show a demo value
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

    def _on_attraction_clicked(self, label: str):
        """Show a small dialog with simulated wait times for the attraction."""
        try:
            # Use the persistent wait time for this attraction label. If
            # for some reason it doesn't exist, generate and store it.
            if label not in self._attraction_waits:
                self._attraction_waits[label] = random.randint(3, 25)
            wait = self._attraction_waits[label]
            text = f"Wachttijd = {wait} minuut"

            dlg = QMessageBox(self)
            dlg.setWindowTitle(f"Wachttijd - {label}")
            dlg.setText(text)
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.exec()
        except Exception:
            pass
