import win32gui
from PySide6.QtCore import QTimer
from frontend.core import suggestion_settings
from frontend.components.suggest_popup import SuggestTaskPopup


class WindowTitleWatcher:
    def __init__(self, api_client, task_timer, floating_control=None):
        self.api_client = api_client
        self.task_timer = task_timer
        self.floating_control = floating_control  # 👈 elmentjük a floating ablakot
        self.previous_title = ""
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_window)
        self.timer.start(5000)  # 1 percenként ellenőrzünk

    def get_active_window_title(self):
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)

    def check_window(self):
        current_title = self.get_active_window_title()
        if current_title == self.previous_title:
            return

        self.previous_title = current_title

        # ⛔ Ne ajánljunk, ha fut task vagy nincs engedélyezve
        if self.task_timer.get_active_task():
            return

        if not suggestion_settings.suggestion_settings.is_suggestion_allowed(current_title):
            return

        popup = SuggestTaskPopup(
            api_client=self.api_client,
            task_timer=self.task_timer,
            window_title=current_title,
            floating_control=self.floating_control  # 👈 átadjuk!
        )
        popup.show_in_front_of_active_window()
        suggestion_settings.suggestion_settings.dismiss_for_now(current_title)
