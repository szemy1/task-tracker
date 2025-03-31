# backend/tests/conftest.py

import sys
import pytest
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session", autouse=True)
def app():
    """Egyszeri QApplication példány a teljes tesztszekcióhoz"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
    app.quit()
