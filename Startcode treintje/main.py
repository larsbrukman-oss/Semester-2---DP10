from PyQt6.QtWidgets import QApplication
from schermen.main_window import MainWindow

def main():
    app = QApplication([])
    load_stylesheet(app)
    window = MainWindow()
    window.show()
    app.exec()

def load_stylesheet(app):
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

if __name__ == "__main__":
    main()