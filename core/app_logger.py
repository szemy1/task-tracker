import time
import threading
import win32gui
from datetime import datetime, timedelta
from core.tag_suggester import suggest_tag

from datetime import datetime, timedelta

class AppLogger(threading.Thread):
    def __init__(self, task_manager, notifier):
        super().__init__()
        self.task_manager = task_manager
        self.notifier = notifier
        self.running = False
        self.last_window = None
        self.dismissed_windows = {} # ⬅️ új mező

    def dismiss_window(self, window_title):
        self.dismissed_windows.add(window_title)

    def run(self):
        self.running = True
        while self.running:
            current_window = self.get_active_window_title()
            if current_window != self.last_window:
                self.last_window = current_window
                tag = suggest_tag(current_window)
                log_msg = f"Aktív ablak: {current_window} → {tag}"
                active_task = self.task_manager.get_active_task()
                if active_task:
                    active_task.log_event(log_msg)
                elif tag == 'fejlesztés' and current_window not in self.dismissed_windows:
                    print(f"[AppLogger] Feladatjavaslat indítása: {current_window}")
                    self.notifier.suggest_task_signal.emit(current_window)
            time.sleep(1)

    def dismiss_window(self, window_title):
        """ Hozzáadjuk az elutasított ablakot a blacklisthez """
        self.dismissed_windows[window_title] = datetime.now()

    def stop(self):
        self.running = False

    @staticmethod
    def get_active_window_title():
        try:
            import win32gui
            window = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(window)
        except:
            return "Ismeretlen"

