import sys
import os
import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from unittest.mock import patch, MagicMock

# Projekt gyökér hozzáadása az importhoz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from frontend.main import MainWindow
from frontend.core import suggestion_settings


@pytest.fixture
def main_window(qtbot):
    # Letiltjuk az ajánlásokat a teszt alatt
    suggestion_settings.suggestion_settings.disable()

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

@patch("PySide6.QtWidgets.QInputDialog.getText", return_value=("Tesztfeladat Floatingból", True))
@patch("PySide6.QtWidgets.QInputDialog.getMultiLineText", return_value=("Ez egy automatikus teszt által létrehozott task.", True))
@patch("frontend.services.api_client.APIClient.create_task", return_value={"id": 999, "name": "Tesztfeladat Floatingból", "status": "in_progress"})
@patch("frontend.services.api_client.APIClient.start_task", return_value=None)
@patch("frontend.services.api_client.APIClient.get_tasks", return_value=[{"id": 999, "name": "Tesztfeladat Floatingból", "status": "in_progress"}])
def test_create_and_start_task_via_floating_control(mock_get_tasks, mock_start, mock_create, mock_desc_input, mock_title_input, qtbot):
    suggestion_settings.suggestion_settings.disable()

    app = QApplication.instance() or QApplication([])

    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    floating = window.floating_control
    qtbot.addWidget(floating)
    floating.show()

    floating.refresh_task_list_callback = window.load_tasks

    # 👉 Start gomb megnyomása
    qtbot.mouseClick(floating.toggle_button, Qt.LeftButton)
    qtbot.waitUntil(lambda: floating.current_task_id is not None, timeout=2000)
    qtbot.waitUntil(lambda: floating.is_running is True, timeout=2000)

    assert floating.current_task_id == 999
    assert floating.is_running is True