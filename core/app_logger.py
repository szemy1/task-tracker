import time
import threading
import win32gui
from datetime import datetime
from core.tag_suggester import suggest_tag

class AppLogger(threading.Thread):
    def __init__(self, task_manager, notifier):
        super().__init__()
        self.task_manager = task_manager
        self.notifier = notifier
        self.running = False
        self.last_window = None

    def run(self):
        self.running = True

        while self.running:
            current_window = self.get_active_window_title()

            if current_window != self.last_window:
                self.last_window = current_window
                tag = suggest_tag(current_window)
                log_msg = f"Aktív ablak: {current_window} | Típus: {tag}"
                
                active_task = self.task_manager.get_active_task()
                if active_task:
                    active_task.log_event(log_msg)
                elif tag == 'munka':
                    # Csak akkor javasolj feladatot, ha nincs aktív feladat és "munka" az ablak típusa
                    self.notifier.suggest_task_signal.emit(current_window)

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
