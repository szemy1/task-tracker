import pytest
from PySide6.QtWidgets import QApplication
from frontend.main import MainWindow

@pytest.fixture
def main_window(qtbot):
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window
