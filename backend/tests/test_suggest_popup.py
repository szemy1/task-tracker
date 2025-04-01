# 📄 backend/tests/test_suggest_popup.py

import sys
import os
import pytest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication, QInputDialog
from frontend.components.suggest_popup import SuggestTaskPopup
from frontend.main import MainWindow


@pytest.fixture
def app_instance():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


def test_suggest_popup_updates_floating_button(qtbot, app_instance):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    floating = window.floating_control
    task_title = "Popup Teszt Feladat"
    task_desc = "Popupból indított teszt"

    with patch.object(QInputDialog, "getMultiLineText", return_value=(task_desc, True)):
        popup = SuggestTaskPopup(
            api_client=window.api_client,
            task_timer=window.task_timer,
            window_title=task_title,
            floating_control=floating,  # 👈 FONTOS!
            parent=window
        )
        qtbot.addWidget(popup)
        popup.title_input.setText(task_title)
        popup.accept()

    # ⏳ Több időt adunk a start műveletnek és a floating ablak frissülésének
    qtbot.waitUntil(lambda: floating.is_running and floating.toggle_button.text() == "⏸️ Stop", timeout=5000)

    assert floating.current_task_id is not None
    assert floating.is_running
    assert floating.toggle_button.text() == "⏸️ Stop"

    # Cleanup
    window.api_client.delete_task(floating.current_task_id)
