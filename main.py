import sys
import json
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt  # ← EZ HIÁNYZOTT
from gui.main_window import MainWindow


def apply_theme(app):
    try:
        with open("config/settings.json", "r") as f:
            settings = json.load(f)
            theme = settings.get("theme", "light")
    except:
        theme = "light"

    if theme == "dark":
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(60, 60, 60))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        app.setPalette(dark_palette)
    else:
        app.setPalette(QPalette())  # visszaáll alap világos témára


def main():
    app = QApplication(sys.argv)
    apply_theme(app)  # <- ITT ALKALMAZZUK A TÉMÁT
    window = MainWindow()
    MainWindow.instance = window
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
