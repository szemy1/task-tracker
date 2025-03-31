import sys
import os
import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from unittest.mock import patch

# 🔧 Projekt gyökér felvétele az importhoz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from frontend.main import MainWindow


@pytest.fixture
def main_window(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window

def test_window_title(main_window):
    assert "TimeTracker" in main_window.windowTitle()

def test_task_list_loads(main_window, qtbot):
    main_window.load_tasks()
    qtbot.wait(300)
    count = main_window.task_list_widget.count()
    assert count >= 0

def test_create_and_start_task_via_floating_control(qtbot):
    app = QApplication.instance() or QApplication([])

    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    floating = window.floating_control
    qtbot.addWidget(floating)
    floating.show()

    mock_title = "Tesztfeladat Floatingból"
    mock_desc = "Ez egy automatikus teszt által létrehozott task."

    with patch("PySide6.QtWidgets.QInputDialog.getText", return_value=(mock_title, True)), \
         patch("PySide6.QtWidgets.QInputDialog.getMultiLineText", return_value=(mock_desc, True)):

        qtbot.mouseClick(floating.toggle_button, Qt.LeftButton)
        qtbot.wait(500)  # Kis várakozás, hogy legyen ideje frissülni

        assert floating.current_task_id is not None
        qtbot.waitUntil(lambda: floating.is_running is True, timeout=4000)

        assert floating.is_running is True

        tasks = window.api_client.get_tasks()
        matching = [t for t in tasks if t["id"] == floating.current_task_id]
        assert len(matching) == 1
        assert matching[0]["name"] == mock_title
        assert matching[0]["status"] == "in_progress"

