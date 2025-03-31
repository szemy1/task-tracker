# backend/core/window_title_watcher.py

from PySide6.QtCore import QObject, QTimer
import win32gui

from frontend.components.suggest_popup import SuggestTaskPopup
from frontend.core.suggestion_settings import suggestion_settings


class WindowTitleWatcher(QObject):
    def __init__(self, api_client, task_timer, interval=5):
        super().__init__()
        self.api_client = api_client
        self.task_timer = task_timer
        self.interval = interval * 1000
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_window)
        self.timer.start()
        self.current_popup = None

    def check_window(self):
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)

        # ⛔ Ne ajánljunk semmit, ha van aktív task
        if self.task_timer.get_active_task():
            return

        if suggestion_settings.is_suggestion_allowed(title):
            self.show_suggest_popup(title)


    def show_suggest_popup(self, window_title):
        if self.current_popup and self.current_popup.isVisible():
            return

        self.current_popup = SuggestTaskPopup(self.api_client, self.task_timer, window_title)
        self.current_popup.rejected.connect(lambda: suggestion_settings.dismiss_for_now(window_title))
        self.current_popup.show_in_front_of_active_window()
