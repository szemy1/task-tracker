# core/app_logger.py

import time
import threading
import win32gui
from datetime import datetime
from core.tag_suggester import suggest_tag


class AppLogger(threading.Thread):
    def __init__(self, task):
        super().__init__()
        self.task = task
        self.running = False
        self.last_window = None

    def run(self):
        self.running = True

        while self.running:
            current_window = self.get_active_window_title()
            timestamp = datetime.now()

            if current_window != self.last_window:
                self.last_window = current_window

                # 🧠 Itt javasolunk címkét
                tag = suggest_tag(current_window)
                log_msg = f"Aktív ablak: {current_window} | Típus: {tag}"

                self.task.log_event(log_msg)

            time.sleep(1)




    def stop(self):
        self.running = False

    @staticmethod
    def get_active_window_title():
        try:
            window = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(window)
        except:
            return "Ismeretlen"
