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


def test_task_selector_populates(main_window, qtbot):
    floating = main_window.floating_control
    qtbot.addWidget(floating)
    floating.refresh_task_list_callback = main_window.load_tasks
    main_window.load_tasks()
    qtbot.wait(500)
    
    assert floating.task_selector.count() > 1  # Az "Új feladat" plusz legalább 1

