"""
scherm2.py

This file implements the 'Volg de trein' screen (Scherm2).

Short human-friendly explanation (written in natural language):
- The main widget shows a simple square 'map' area (drawn manually) and
    a few controls underneath. The map is not a real map service — it's a
    lightweight placeholder that paints a background, grid lines, attraction
    markers and a single black dot that represents the train's estimated
    location.

How to read this file quickly:
- The `Scherm2` class builds the UI layout and wires the buttons.
- The `MapWidget` class does the painting: background, grid, attractions,
    and the train dot. Coordinates for attractions and the train are
    normalized (0.0..1.0) relative to the widget size.

If you want to change behavior:
- Update `self.attractions` inside `Scherm2.__init__` to add/remove attractions.
- Change the random movement in `ververs_locatie` to follow a recorded path.
- Replace the placeholder drawing in `MapWidget.paintEvent` with an image
    or a real map widget if you want higher fidelity.

The comments in this file are written in plain language so another
developer (or you in a few days) can understand what each part does.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QBrush, QColor
import random


class Scherm2(QWidget):
    """Main screen for following the train.

    This class builds the layout: a central map area and some buttons below it.
    I wrote the comments so they read like a colleague explaining the code:
    short, practical and actionable.
    """

    def __init__(self, main_window):
        # Standard QWidget initialisation.
        super().__init__()
        self.main_window = main_window

        # Vertical layout: map at the top (centered), control buttons below.
        layout = QVBoxLayout()

        # Give the map a little breathing room from the top of the window.
        layout.addStretch(1)

        # Create a horizontal container for the map to keep it centered.
        # The map itself is a custom widget (MapWidget) that handles its own
        # painting. We add stretch on both sides so the map stays centered.
        self.map_container = QHBoxLayout()
        self.map_container.addStretch(1)
        self.map_widget = MapWidget()
        self.map_container.addWidget(self.map_widget)
        self.map_container.addStretch(1)
        layout.addLayout(self.map_container)

        # ------------------------------------------------------------------
        # Attractions: these are example points on the map. Coordinates are
        # normalized between 0.0 and 1.0 so they work regardless of widget size.
        # To change the attractions, edit this list: (x, y, label).
        # ------------------------------------------------------------------
        self.attractions = [
            (0.2, 0.2, "Rollercoaster"),
            (0.8, 0.25, "Ferris Wheel"),
            (0.5, 0.7, "Haunted House"),
        ]
        # Tell the map widget to draw these attractions.
        self.map_widget.set_attractions(self.attractions)

        # Small spacing between map and buttons — keeps the UI airy.
        layout.addSpacing(12)

        # ------------------------------------------------------------------
        # Middle row: two important actions sit side-by-side under the map:
        # - 'Volg de trein' updates the train position (right now it randomizes)
        # - 'Vergroot' goes to the zoom screen (scherm4)
        # I keep both buttons the same visual size so the UI feels balanced.
        # ------------------------------------------------------------------
        middle_row = QHBoxLayout()
        middle_row.addStretch(1)

        btn_ververs = QPushButton("Volg de trein")
        btn_ververs.setFixedSize(200, 50)
        # When the user clicks this, we refresh the train location.
        btn_ververs.clicked.connect(self.ververs_locatie)
        btn_ververs.setStyleSheet(
            "QPushButton{background-color: #28a745; color: white; border-radius: 25px; font-weight: 600;}"
        )
        middle_row.addWidget(btn_ververs)

        middle_row.addSpacing(12)

        self.vergroot_btn = QPushButton("Vergroot")
        self.vergroot_btn.setFixedSize(200, 50)
        # This currently navigates to scherm4. Later we could make it zoom in-place.
        self.vergroot_btn.clicked.connect(self.open_scherm4)
        self.vergroot_btn.setStyleSheet("QPushButton{background-color: #0069d9; color: white; border-radius: 25px;}" )
        middle_row.addWidget(self.vergroot_btn)

        middle_row.addStretch(1)
        layout.addLayout(middle_row)

        # A bit of flexible space so the map stays visually dominant.
        layout.addStretch(1)

        # ------------------------------------------------------------------
        # Lower row: a centered 'Reserveer' button. This is a placeholder
        # for a reservation flow — feel free to wire it to a real page.
        # ------------------------------------------------------------------
        lower_row = QHBoxLayout()
        lower_row.addStretch(1)
        btn_reserveer = QPushButton("Reserveer")
        btn_reserveer.setFixedSize(200, 50)
        # By default this navigates to scherm3 in the app stack.
        btn_reserveer.clicked.connect(self.open_scherm)
        btn_reserveer.setStyleSheet(
            "QPushButton{background-color: #28a745; color: white; border-radius: 25px; font-weight: 600;}"
        )
        lower_row.addWidget(btn_reserveer)
        lower_row.addStretch(1)
        layout.addLayout(lower_row)

        # Apply the composed layout to the widget.
        self.setLayout(layout)

        # ------------------------------------------------------------------
        # Initial state: place the train roughly in the middle of the map.
        # Coordinates are normalized (0..1) so the widget will draw the dot
        # at the correct pixel location in `MapWidget.paintEvent`.
        # ------------------------------------------------------------------
        self.current_pos = (0.5, 0.5)
        self.map_widget.set_dot_normalized(*self.current_pos)

    def resizeEvent(self, event):
        """Handle window resizes.

        We make the map a square whose side is a portion of the main window
        height so the map scales sensibly when the user resizes the window.
        """
        try:
            # make the map approximately 55% of the main window height
            h = max(220, int(self.main_window.size().height() * 0.55))
        except Exception:
            # Fallback: if main_window isn't available for some reason, use
            # this widget's own height as the base for sizing.
            h = max(220, int(self.size().height() * 0.55))

        # Keep the map square.
        self.map_widget.setFixedSize(h, h)
        super().resizeEvent(event)

    def position_vergroot_button(self):
        """Legacy helper (kept for reference).

        Previous layouts positioned the 'Vergroot' button as a child of the map
        and required manual centering. In the current layout the button sits
        under the map, so this method is kept for backward compatibility only.
        """
        # No work necessary in the current layout; function left intentionally
        # as documentation for earlier behavior.
        return

    def ververs_locatie(self):
        """Refresh the train's estimated location.

        Right now this simply picks a random location on the map. In a real
        application you'd replace this with the latest estimate from your
        backend or a simulated route.
        """
        x = random.random()
        y = random.random()
        self.current_pos = (x, y)
        # Tell the map widget to repaint with the new dot position.
        self.map_widget.set_dot_normalized(x, y)

    def open_scherm4(self):
        """Navigate to screen 4 (zoomed view).

        The button labeled 'Vergroot' triggers this. Currently it just asks
        the main window to show `scherm4` (that screen exists in the app
        stack). If you want in-place zoom instead, we can implement that.
        """
        if hasattr(self, 'main_window') and self.main_window:
            try:
                self.main_window.toon_pagina(self.main_window.scherm4)
            except Exception:
                # Silently ignore navigation errors in this simple demo.
                pass

    def open_scherm(self):
        """Navigate to screen 3 (placeholder for reservation flow).

        This method is a thin wrapper that asks the main window to switch
        the visible page in the stacked widget. It's intentionally simple;
        error handling is kept minimal for clarity.
        """
        if hasattr(self, 'main_window') and self.main_window:
            try:
                self.main_window.toon_pagina(self.main_window.scherm3)
            except Exception:
                pass


class MapWidget(QWidget):
    """A tiny, self-contained drawing surface that simulates a map.

    Implementation notes (human tone):
    - The widget paints a light background, faint grid lines and a thick
      border so the map stands out visually.
    - The train is a black dot, whose logical position is stored as
      normalized coordinates (x, y) in `self._dot`. Normalized means:
        0.0 = left/top, 1.0 = right/bottom.
    - Attractions are optional: pass a list like [(x,y,label), ...]
      to `set_attractions()` and the widget will draw small red markers
      with a label next to each marker.

    This widget is intentionally small and dependency-free: it doesn't use
    Qt's web engine or map APIs. It's perfect for prototypes and demo UIs.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Default train position centered in the map (normalized coords).
        self._dot = (0.5, 0.5)
        # Set a comfortable minimum size so the map looks good on small windows.
        self.setMinimumSize(220, 220)

    def set_dot_normalized(self, x, y):
        """Update the train position (normalized coords) and repaint.

        We clamp inputs to the [0, 1] range to avoid drawing outside the widget.
        """
        x = min(max(0.0, float(x)), 1.0)
        y = min(max(0.0, float(y)), 1.0)
        self._dot = (x, y)
        self.update()  # schedule a repaint

    def set_attractions(self, attractions):
        """Provide a list of attractions for the map to draw.

        Each attraction is a tuple: (x, y, label) with normalized x/y.
        """
        self._attractions = attractions
        self.update()

    def paintEvent(self, event):
        """Draw the whole map every time Qt asks us to paint.

        The drawing order is: background -> border -> grid -> train dot ->
        attraction markers and labels. That keeps the dot clearly visible.
        """
        painter = QPainter(self)

        # Background and a slightly darker border so the map stands out.
        painter.setBrush(QBrush(QColor(230, 230, 230)))
        pen = painter.pen()
        pen.setColor(QColor(160, 160, 160))
        pen.setWidth(4)
        painter.setPen(pen)
        painter.drawRect(self.rect())

        # Subtle grid lines to make the placeholder feel map-like.
        grid_pen = painter.pen()
        grid_pen.setColor(QColor(210, 210, 210))
        grid_pen.setWidth(1)
        painter.setPen(grid_pen)
        w = self.width()
        h = self.height()
        for i in range(1, 4):
            painter.drawLine(int(w * i / 4), 0, int(w * i / 4), h)
            painter.drawLine(0, int(h * i / 4), w, int(h * i / 4))

        # Draw the train as a black circle. Radius scales with widget size.
        dot_x = int(self._dot[0] * w)
        dot_y = int(self._dot[1] * h)
        radius = max(10, int(min(w, h) * 0.045))
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.setPen(Qt.GlobalColor.black)
        painter.drawEllipse(dot_x - radius, dot_y - radius, radius * 2, radius * 2)

        # Draw attraction markers (if provided). Markers are small red dots
        # with plain text labels to the right. If you want richer labels
        # (background boxes, fonts), we can add that easily.
        if hasattr(self, '_attractions') and self._attractions:
            marker_radius = max(6, int(min(w, h) * 0.03))
            painter.setBrush(QBrush(QColor(200, 30, 30)))
            painter.setPen(Qt.GlobalColor.black)
            for (ax, ay, label) in self._attractions:
                mx = int(ax * w)
                my = int(ay * h)
                # marker
                painter.drawEllipse(mx - marker_radius, my - marker_radius, marker_radius * 2, marker_radius * 2)
                # label — simple and readable
                painter.drawText(mx + marker_radius + 4, my + marker_radius // 2, label)

    
