from PyQt6.QtWidgets import QApplication
from schermen.main_window import MainWindow


#Regel 1 & 2 = imports : haalt dingen op die nodig zijn om een venster te maken 
#na from krijg je de import locatie, na import krijg je wat je import

def main():
    app = QApplication([])
    load_stylesheet(app)
    window = MainWindow()
    window.show()
    app.exec()

#Regel 8 tm 13 = Main() Functie : Regel 9 : Qappl is het hart van de app
#Regel 10 : laadt een stylesheet, regel 11 :maakt het hoofdvenster, Regel 12 : laadt het venster zien
#Regel 13 : start de eventloop zodat de app reageert

def load_stylesheet(app):
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

#Regel 19-21 = Load_stylesheet() (Functie) : opent het bestand style.qss en gebruikt dat
#om de stijl van de app te bepalen

if __name__ == "__main__":
    main()

#Regel 26-27 = start de app : zorgt dat main() alleen wordt uitgevoerd als je main direct start

print("Dit is een test voor git")