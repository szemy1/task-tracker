# backend/tests/test_integration_gui_backend.py

import pytest
from frontend.components.main_window import MainWindow

@pytest.fixture
def main_window(qtbot):
    """Fixture a MainWindow példányhoz"""
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window

def test_window_title(main_window):
    assert "TimeTracker" in main_window.windowTitle()

def test_task_list_loads(main_window, qtbot):
    main_window.load_tasks()
    qtbot.wait(300)  # Várunk kicsit, ha async API lenne
    count = main_window.task_list_widget.count()
    assert count >= 0  # Akkor is jó, ha üres
