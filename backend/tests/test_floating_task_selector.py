# backend/tests/test_floating_task_selector.py

from PySide6.QtWidgets import QApplication
import pytest
from frontend.components.floating_control_window import FloatingControlWindow
from frontend.services.api_client import APIClient
from frontend.core.task_timer_manager import TaskTimerManager


@pytest.fixture
def floating_window(qtbot):
    app = QApplication.instance() or QApplication([])
    window = FloatingControlWindow(TaskTimerManager(), lambda: None, APIClient())
    qtbot.addWidget(window)
    window.show()
    return window


def test_task_selector_populates(floating_window, qtbot):
    mock_tasks = [
        {"id": 1, "name": "Teszt 1", "status": "todo"},
        {"id": 2, "name": "Teszt 2", "status": "in_progress"},
    ]
    floating_window.update_task_list(mock_tasks)

    qtbot.wait(200)

    count = floating_window.task_selector.count()
    assert count == 3  # 🆕 + 2 task
    assert floating_window.task_selector.itemText(1) == "Teszt 1 (1)"
    assert floating_window.task_selector.itemData(2) == 2
