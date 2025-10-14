# --- written by assistant ---
# This file contains the code that was added to `scherm2.py` by the assistant.
# Purpose: standalone copy so you can easily separate assistant-generated code
# from the original project files. The code below is safe to read and copy.

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QBrush, QColor
import random


class Scherm2_Assistant(QWidget):
    """Replica of the assistant-added UI for Scherm2.

    Use this as a reference. It is not wired into the app automatically.
    Copy the relevant parts into your `scherm2.py` if you want to replace the
    existing screen.
    """
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        layout.addStretch(1)

        title = QLabel("Volg het treintje")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(title)

        # Map area: centered horizontally, occupies ~25% of main window height as a square
        self.map_container = QHBoxLayout()
        self.map_container.addStretch(1)
        self.map_widget = MapWidget()
        self.map_container.addWidget(self.map_widget)
        self.map_container.addStretch(1)
        layout.addLayout(self.map_container)

        # Ververs button below the map
        btn_ververs = QPushButton("Ververs")
        btn_ververs.setFixedSize(120, 40)
        btn_ververs.clicked.connect(self.ververs_locatie)
        layout.addWidget(btn_ververs, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addStretch(3)

        # Navigation example (keeps original button to go to scherm3)
        btn_naar_scherm3 = QPushButton("Naar scherm 3")
        btn_naar_scherm3.clicked.connect(self.open_scherm)
        layout.addWidget(btn_naar_scherm3, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

        # initial position of the train (normalized coordinates 0..1)
        self.current_pos = (0.5, 0.5)
        self.map_widget.set_dot_normalized(*self.current_pos)

    def resizeEvent(self, event):
        # Adjust the map widget size so it occupies ~25% of the main window height and stays centered
        try:
            h = max(100, int(self.main_window.size().height() * 0.25))
        except Exception:
            h = max(100, int(self.size().height() * 0.25))
        # make the map square
        self.map_widget.setFixedSize(h, h)
        super().resizeEvent(event)

    def ververs_locatie(self):
        # Randomize the train location inside the map (normalized coordinates)
        x = random.random()
        y = random.random()
        self.current_pos = (x, y)
        self.map_widget.set_dot_normalized(x, y)

    def open_scherm(self):
        if self.main_window:
            try:
                self.main_window.toon_pagina(self.main_window.scherm3)
            except Exception:
                pass


class MapWidget(QWidget):
    """Simple placeholder map widget that draws a light background and a black dot for the train."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._dot = (0.5, 0.5)  # normalized position (0..1, 0..1)
        self.setMinimumSize(120, 120)

    def set_dot_normalized(self, x, y):
        # clamp
        x = min(max(0.0, float(x)), 1.0)
        y = min(max(0.0, float(y)), 1.0)
        self._dot = (x, y)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        # background map area
        painter.setBrush(QBrush(QColor(230, 230, 230)))
        painter.setPen(QColor(180, 180, 180))
        painter.drawRect(self.rect())

        # draw a simple grid (optional subtle map)
        pen = painter.pen()
        pen.setColor(QColor(210, 210, 210))
        painter.setPen(pen)
        w = self.width()
        h = self.height()
        for i in range(1, 4):
            painter.drawLine(int(w * i / 4), 0, int(w * i / 4), h)
            painter.drawLine(0, int(h * i / 4), w, int(h * i / 4))

        # draw dot
        dot_x = int(self._dot[0] * w)
        dot_y = int(self._dot[1] * h)
        radius = max(6, int(min(w, h) * 0.03))
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.setPen(Qt.GlobalColor.black)
        painter.drawEllipse(dot_x - radius, dot_y - radius, radius * 2, radius * 2)


# --- end of assistant code ---
