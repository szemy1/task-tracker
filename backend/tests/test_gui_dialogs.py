# backend/tests/test_gui_dialogs.py

import unittest
from PySide6.QtWidgets import QApplication
from frontend.components.new_task_dialog import NewTaskDialog
from frontend.components.edit_task_dialog import EditTaskDialog
from frontend.components.log_window import LogWindow
from unittest.mock import MagicMock

import sys
app = QApplication.instance() or QApplication(sys.argv)


class TestDialogs(unittest.TestCase):

    def setUp(self):
        self.api_mock = MagicMock()

    def test_new_task_dialog_opens(self):
        dialog = NewTaskDialog(api_client=self.api_mock)
        self.assertTrue(dialog.windowTitle())  # Ellenőrizzük, hogy van címe

    def test_edit_task_dialog_opens(self):
        sample_task = {
            "id": 1,
            "name": "Teszt Task",
            "description": "Leírás",
            "status": "open"
        }
        dialog = EditTaskDialog(api_client=self.api_mock, task=sample_task)
        self.assertEqual(dialog.windowTitle(), "Feladat szerkesztése")

    def test_log_window_opens(self):
        log_window = LogWindow()
        self.assertIn("log", log_window.windowTitle().lower())  # kisbetűs összehasonlítás


if __name__ == "__main__":
    unittest.main()
