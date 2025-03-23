import sys
from PySide6.QtWidgets import QApplication, QSplashScreen, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QTimer
from gui.main_window import MainWindow
#from core.settings import load_settings, save_settings
import os

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

    # Tálcaikon létrehozása
    tray_icon = QSystemTrayIcon(QIcon("icon.png"))
    tray_menu = QMenu()
    tray_open = tray_menu.addAction("Megnyitás")
    tray_exit = tray_menu.addAction("Kilépés")
    tray_open.triggered.connect(window.show)
    tray_exit.triggered.connect(app.quit)
    tray_icon.setContextMenu(tray_menu)
    tray_icon.show()

    # Tálca menü
    menu = QMenu()
    open_action = QAction("Feladatkezelő megnyitása")
    exit_action = QAction("Kilépés")

    menu.addAction(open_action)
    menu.addAction(exit_action)

    tray_icon.setContextMenu(menu)

    open_action.triggered.connect(window.show)
    exit_action.triggered.connect(app.quit)

    tray_icon.activated.connect(lambda reason: window.show() if reason == QSystemTrayIcon.DoubleClick else None)
    tray_icon.show()

    window.show()

    sys.exit(app.exec())

def start_main_window(splash, window):
    splash.close()
    window.show()

if __name__ == "__main__":
    main()
