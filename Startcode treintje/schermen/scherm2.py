"""
scherm2.py

Dit bestand implementeert het 'Volg de trein' scherm (Scherm2).

Korte, mensvriendelijke uitleg:
- De hoofdwidget toont een eenvoudige vierkante 'kaart' (handmatig getekend)
    met een paar knoppen eronder. Dit is geen echte kaartdienst maar een
    lichte placeholder: achtergrond, rasterlijnen, attractiemarkeringen en
    een zwarte stip die de geschatte positie van de trein weergeeft.

Hoe dit bestand snel te lezen:
- De klasse `Scherm2` bouwt de UI-layout en koppelt de knoppen.
- De klasse `MapWidget` doet het tekenen: achtergrond, raster, attracties
    en de treindot. Coördinaten voor attracties en de trein zijn genormaliseerd
    (0.0..1.0) ten opzichte van de widgetgrootte.

Als je gedrag wilt aanpassen:
- Pas `self.attractions` in `Scherm2.__init__` aan om attracties toe te voegen/verwijderen.
- Vervang de random beweging in `ververs_locatie` door een opgenomen route.
- Vervang de placeholder-tekening in `MapWidget.paintEvent` door een afbeelding
    of een echte kaartwidget voor hogere nauwkeurigheid.

De opmerkingen in dit bestand zijn in begrijpelijk Nederlands geschreven zodat
een andere ontwikkelaar (of jijzelf later) snel kan begrijpen wat er gebeurt.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QBrush, QColor
import random


class Scherm2(QWidget):
    # Signal emitted whenever the train position or info is refreshed.
    # Emits (train_info: dict, position: tuple(x,y))
    train_updated = pyqtSignal(dict, tuple)
    """Hoofdscherm om de trein te volgen.

    Deze klasse bouwt de layout: een centraal kaartgebied met knoppen eronder.
    De opmerkingen zijn beknopt en praktisch zodat de code makkelijk te volgen is.
    """

    def __init__(self, main_window):
        # Standard QWidget initialisation.
        super().__init__()
        self.main_window = main_window

        # Vertical layout: map at the top (centered), control buttons below.
    # Verticale layout: kaart bovenin (gecentreerd), bedieningsknoppen eronder.
        layout = QVBoxLayout()

        # Top row: left-aligned back button that returns to the start screen.
    # Bovenste rij: terugknop linksboven die naar het startscherm teruggaat.
        top_row = QHBoxLayout()
        self.btn_terug_top = QPushButton("Terug")
        self.btn_terug_top.setFixedSize(120, 40)
        self.btn_terug_top.setStyleSheet("QPushButton{background-color: #28a745; color: white; border-radius: 20px; font-weight: 600;}")
        # Wire to startscherm
        self.btn_terug_top.clicked.connect(lambda: self.main_window.toon_pagina(self.main_window.startscherm))
        top_row.addWidget(self.btn_terug_top)
        top_row.addStretch(1)
        layout.addLayout(top_row)

        # Give the map a little breathing room from the top of the window.
    # Geef de kaart wat ruimte vanaf de bovenkant van het venster.
        layout.addStretch(1)

        # Create a horizontal container for the map to keep it centered.
    # Maak een horizontale container zodat de kaart gecentreerd blijft.
    # De kaart is een custom widget (`MapWidget`) die zelf tekent. We
    # plaatsen stretches aan beide zijden om centering af te dwingen.
        self.map_container = QHBoxLayout()
        self.map_container.addStretch(1)
        self.map_widget = MapWidget()
        self.map_container.addWidget(self.map_widget)
        self.map_container.addStretch(1)
        layout.addLayout(self.map_container)

        # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Attracties: voorbeeldpunten op de kaart. Coördinaten zijn genormaliseerd
    # tussen 0.0 en 1.0 zodat ze werken ongeacht widgetgrootte. Pas deze lijst
    # aan om attracties toe te voegen of te verwijderen: (x, y, label).
        # ------------------------------------------------------------------
        self.attractions = [
            (0.2, 0.2, "Rollercoaster"),
            (0.8, 0.25, "Ferris Wheel"),
            (0.5, 0.7, "Haunted House"),
        ]
        # Tell the map widget to draw these attractions.
    # Geef de kaartwidget door welke attracties getekend moeten worden.
        self.map_widget.set_attractions(self.attractions)

        # Example platforms (perrons). We'll draw them as point markers
    # Voorbeeldperrons. We tekenen deze als puntmarkeringen (zoals attracties)
    # zodat de kaart overzichtelijk blijft. Iedere entry is (x, y, label).
        self.platforms = [
            (0.12, 0.86, "Perron 1"),
            (0.88, 0.86, "Perron 2"),
        ]
        # Tell the map widget to draw platforms as point markers.
        self.map_widget.set_platforms(self.platforms)
    # Geef de kaartwidget de perrons door en houd reserveringen per perron bij.
    # Reserveringen starten op nul; de keys zijn perronlabels.
        self.reservations = {label: 0 for (_, _, label) in self.platforms}

        # Small spacing between map and buttons — keeps the UI airy.
    # Kleine ruimte tussen kaart en knoppen — houdt de UI luchtig.
        layout.addSpacing(12)

        # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Middenrij: twee belangrijke acties naast elkaar onder de kaart:
    # - 'Volg de trein' ververst de treinkpositie (nu random)
    # - 'Vergroot' opent het vergrote kaartscherm (scherm4)
    # Beide knoppen hebben gelijke afmetingen voor visuele balans.
        # ------------------------------------------------------------------
        middle_row = QHBoxLayout()
        middle_row.addStretch(1)

        btn_ververs = QPushButton("Volg de trein")
        btn_ververs.setFixedSize(200, 50)
        # When the user clicks this, we refresh the train location.
    # Wanneer de gebruiker klikt, verversen we de treinlocatie.
        btn_ververs.clicked.connect(self.ververs_locatie)
        btn_ververs.setStyleSheet(
            "QPushButton{background-color: #28a745; color: white; border-radius: 25px; font-weight: 600;}"
        )
        middle_row.addWidget(btn_ververs)

        middle_row.addSpacing(12)

        self.vergroot_btn = QPushButton("Vergroot")
        self.vergroot_btn.setFixedSize(200, 50)
        # This currently navigates to scherm4. Later we could make it zoom in-place.
    # Op dit moment navigeert dit naar scherm4. Later kan dit in-place zoomen.
        self.vergroot_btn.clicked.connect(self.open_scherm4)
        self.vergroot_btn.setStyleSheet("QPushButton{background-color: #0069d9; color: white; border-radius: 25px;}" )
        middle_row.addWidget(self.vergroot_btn)

        middle_row.addStretch(1)
        layout.addLayout(middle_row)

        # A bit of flexible space so the map stays visually dominant.
    # Een flexibele ruimte zodat de kaart visueel dominant blijft.
        layout.addStretch(1)

        # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Onderste rij: een gecentreerde 'Reserveer' knop. Placeholder voor de
    # reserveringsflow — koppel gerust aan een echte pagina.
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
    # Stel de samengestelde layout in op de widget.
        self.setLayout(layout)

        # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Initiële staat: plaats de trein ongeveer in het midden van de kaart.
    # Coördinaten zijn genormaliseerd (0..1) zodat de dot correct wordt
    # getekend in `MapWidget.paintEvent`.
    # ------------------------------------------------------------------
        self.current_pos = (0.5, 0.5)
        self.map_widget.set_dot_normalized(*self.current_pos)

        # Small initial train info; seats and arrival time are simulated.
        self.train_info = {"seats_available": 20, "total_seats": 20, "arrival_minutes": 0}
        # Ensure the map widget knows the initial train info as well.
        try:
            self.map_widget.set_train_info(self.train_info)
        except Exception:
            pass

    def get_train_info(self):
        """Geef de huidige gesimuleerde treininfo als dict terug."""
        return getattr(self, 'train_info', {"seats_available": 0, "total_seats": 20, "arrival_minutes": 0})

    def resizeEvent(self, event):
        """Afhandelen van venstergrootte-wijzigingen.

        We maken de kaart vierkant met een zijde die een deel van de
        hoofdvensterhoogte is, zodat de kaart voorspelbaar schaalt.
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
        """Legacy helper (blijft ter referentie).

        Eerdere layouts plaatsten de 'Vergroot' knop als kind van de kaart
        en vroegen handmatige centrering. In de huidige layout staat de knop
        onder de kaart; deze functie is ter documentatie bewaard.
        """
        # Geen actie nodig in de huidige layout; functie is documentatief.
        return

    def ververs_locatie(self):
        """Ververs de geschatte positie van de trein.

        Op dit moment kiezen we een willekeurige locatie. In een echte
        applicatie vervang je dit door de laatste schatting van de backend
        of een gesimuleerde route.
        """
        x = random.random()
        y = random.random()
        self.current_pos = (x, y)
        # Vraag de kaartwidget de nieuwe treindot te tekenen.
        self.map_widget.set_dot_normalized(x, y)
        # Werk gesimuleerde treininfo bij bij verversen. Voor demo randomiseren
        # we het aantal beschikbare zitplaatsen en aankomsttijd.
        seats = random.randint(0, 20)
        minutes = random.randint(1, 12)
        # kies een willekeurig bestemmingsperron en een aantal reserveringen
        dest_label = None
        reservations_for_dest = 0
        try:
            if hasattr(self, 'platforms') and self.platforms:
                dest_label = random.choice(self.platforms)[2]
                # stel een voorstel voor reserveringen vast voor die bestemming
                proposed = random.randint(0, 15)
                # zorg dat (aan boord) + voorgestelde reserveringen <= totale plaatsen
                onboard = 20 - seats
                max_allowed_reservations = max(0, 20 - onboard)
                reservations_for_dest = min(proposed, max_allowed_reservations)
                # werk de opgeslagen reserveringen per station bij
                self.reservations[dest_label] = reservations_for_dest
        except Exception:
            dest_label = None

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
        # Informeer luisteraars (bijv. scherm4) dat de trein is bijgewerkt.
        try:
            self.train_updated.emit(self.train_info, self.current_pos)
        except Exception:
            pass

    def open_scherm4(self):
        """Navigeer naar scherm 4 (vergroot weergave)."""
        # De 'Vergroot' knop roept dit aan. Momenteel vraagt dit het hoofdvenster
        # om `scherm4` te tonen. Voor in-place zoomen kan dit later worden aangepast.
        if hasattr(self, 'main_window') and self.main_window:
            try:
                self.main_window.toon_pagina(self.main_window.scherm4)
            except Exception:
                # Silently ignore navigation errors in this simple demo.
                pass

    def open_scherm(self):
        """Navigeer naar scherm 3 (placeholder voor reserveringsflow)."""
        # Deze methode vraagt het hoofdvenster de zichtbare pagina in de stack te wisselen.
        if hasattr(self, 'main_window') and self.main_window:
            try:
                self.main_window.toon_pagina(self.main_window.scherm3)
            except Exception:
                pass


class MapWidget(QWidget):
    # Signal emitted when the train dot is clicked. Sends the current train_info dict.
    train_clicked = pyqtSignal(dict)
    # Signal emitted when an attraction marker is clicked. Sends the attraction label.
    attraction_clicked = pyqtSignal(str)
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
        # optional metadata about the train; used when the user clicks the train
        self._train_info = {"seats_available": 20, "total_seats": 20, "arrival_minutes": 0}

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

    def set_train_info(self, info: dict):
        """Store arbitrary train info that will be emitted when the train is clicked."""
        self._train_info = dict(info) if info is not None else {}
        self.update()

    def set_platforms(self, platforms):
        """Provide a list of platforms (perrons) to draw.
        Each platform is a tuple: (x, y, label) with normalized coords. Platforms
        are drawn as point markers (like attractions) in this UI.
        """
        self._platforms = platforms
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

        # record the last drawn dot area for hit-testing in mouse events
        self._last_dot_rect = (dot_x - radius, dot_y - radius, radius * 2, radius * 2)

        # Draw attraction markers (if provided). Markers are small red dots
        # with plain text labels to the right. If you want richer labels
        # (background boxes, fonts), we can add that easily.
        # Keep a list of last drawn attraction positions to support click
        # hit-testing in mousePressEvent.
        self._last_attraction_positions = []
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
                # store for hit-testing: (center_x, center_y, radius, label)
                self._last_attraction_positions.append((mx, my, marker_radius, label))

        # Draw platforms (perrons) as blue point markers (similar to
        # attractions) so they are visually consistent and compact.
        if hasattr(self, '_platforms') and self._platforms:
            platform_marker_radius = max(6, int(min(w, h) * 0.03))
            painter.setBrush(QBrush(QColor(50, 120, 220)))
            painter.setPen(Qt.GlobalColor.black)
            for (px, py, plabel) in self._platforms:
                mx = int(px * w)
                my = int(py * h)
                painter.drawEllipse(mx - platform_marker_radius, my - platform_marker_radius, platform_marker_radius * 2, platform_marker_radius * 2)
                painter.drawText(mx + platform_marker_radius + 4, my + platform_marker_radius // 2, plabel)

    def mousePressEvent(self, event):
        """Detect clicks on the train dot and emit `train_clicked` with info.

        This is a simple bounding-box hit test. For a more precise hit-test
        we could compute distance from the dot center.
        """
        try:
            x = event.position().x()
            y = event.position().y()
        except Exception:
            # Fallback for older Qt versions
            x = event.x()
            y = event.y()

        if hasattr(self, '_last_dot_rect'):
            rx, ry, rw, rh = self._last_dot_rect
            if rx <= x <= rx + rw and ry <= y <= ry + rh:
                # Emit the stored train info when the train dot is clicked.
                try:
                    self.train_clicked.emit(getattr(self, '_train_info', {}))
                except Exception:
                    pass
                return
        # Check attractions (circular hit test)
        try:
            if hasattr(self, '_last_attraction_positions'):
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
        # not the train — pass to base class
        super().mousePressEvent(event)

    
