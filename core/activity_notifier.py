from PySide6.QtCore import QObject, Signal

class ActivityNotifier(QObject):
    suggest_task_signal = Signal(str)

    def suggest_task(self, app_name):
        print(f"[NOTIFIER] Javasolt új feladat: {app_name}")  # Debug log
        self.suggest_task_signal.emit(app_name)
