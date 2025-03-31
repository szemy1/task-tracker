from frontend.components.main_window import MainWindow
from frontend.services.api_client import APIClient
from PySide6.QtWidgets import QApplication
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
