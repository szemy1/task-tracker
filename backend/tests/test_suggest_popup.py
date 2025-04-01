# 📄 backend/tests/test_suggest_popup.py

import sys
import os
import pytest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from frontend.components.suggest_popup import SuggestTaskPopup
from frontend.main import MainWindow


@pytest.fixture
def app_instance():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


# 📄 backend/tests/test_suggest_popup.py

def test_suggest_popup_updates_floating_button(qtbot):
    from frontend.main import MainWindow
    from PySide6.QtWidgets import QInputDialog

    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    task_title = "Popup Teszt Feladat"
    task_desc = "Popupból indított teszt"

    with patch.object(QInputDialog, "getMultiLineText", return_value=(task_desc, True)):
        popup = SuggestTaskPopup(
            api_client=window.api_client,
            task_timer=window.task_timer,
            window_title=task_title,
            parent=window
        )
        qtbot.addWidget(popup)
        popup.title_input.setText(task_title)
        popup.accept()

        floating = window.floating_control
        qtbot.waitUntil(lambda: floating.is_running, timeout=2000)
        assert floating.toggle_button.text() == "⏸️ Stop"
        assert task_title in floating.task_selector.currentText()

        task = next(t for t in window.api_client.get_tasks() if t["name"] == task_title)
        window.api_client.stop_task(task["id"])
        window.api_client.delete_task(task["id"])



