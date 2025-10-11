from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class Scherm1(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Dit is scherm 1"))

        self.setLayout(layout)
