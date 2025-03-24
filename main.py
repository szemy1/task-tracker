import sys
from PySide6.QtWidgets import QApplication, QSplashScreen, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QTimer
from gui.main_window import MainWindow
#from core.settings import load_settings, save_settings
import os
import markdown
import html.parser


def main():
    app = QApplication(sys.argv)

    # Splash Screen
    splash_pix = QPixmap("logo.png")
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()

    # Main window betöltése késleltetve (2 másodperc után)
    window = MainWindow()
    QTimer.singleShot(2000, lambda: start_main_window(splash, window))

    # Végül indítsuk el az appot
    sys.exit(app.exec())


def start_main_window(splash, window):
    splash.close()
    window.show()

if __name__ == "__main__":
    main()
