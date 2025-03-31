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


def test_suggest_task_popup_creates_and_starts_task(qtbot, app_instance):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    mock_title = "Test Suggest Task"
    mock_desc = "Leírás automatikus teszthez"

    popup = SuggestTaskPopup(
        api_client=window.api_client,
        task_timer=window.task_timer,
        window_title=mock_title
    )
    qtbot.addWidget(popup)

    popup.title_input.setText(mock_title)

    with patch("PySide6.QtWidgets.QInputDialog.getMultiLineText", return_value=(mock_desc, True)):
        popup.accept()
        qtbot.wait(300)

    tasks = window.api_client.get_tasks()
    found = [t for t in tasks if t["name"] == mock_title]
    assert found, "A létrehozott feladat nem található"

    task = found[0]
    assert task["status"] == "in_progress"

    # 🧹 Cleanup
    window.api_client.delete_task(task["id"])
