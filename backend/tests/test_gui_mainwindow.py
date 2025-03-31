# backend/tests/test_gui_mainwindow.py
# backend/tests/test_gui_mainwindow.py

import unittest
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QPushButton
from frontend.components.main_window import MainWindow
import sys

class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        self.window = MainWindow()

    def tearDown(self):
        self.window.close()

    def test_window_title(self):
        self.assertEqual(self.window.windowTitle(), "TimeTracker GUI")

    def test_task_list_widget_exists(self):
        self.assertIsNotNone(self.window.task_list_widget)

    def test_buttons_exist(self):
        buttons = self.window.findChildren(QPushButton)
        self.assertGreaterEqual(len(buttons), 3)  # refresh, add, delete (esetleg log is)

if __name__ == "__main__":
    unittest.main()
