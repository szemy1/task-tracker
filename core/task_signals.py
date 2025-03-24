# core/task_signals.py

from PySide6.QtCore import QObject, Signal

class TaskSignals(QObject):
    task_started = Signal(dict)  # {"name": ..., "start_time": ...}
    task_stopped = Signal()

# Singleton példány
task_signals = TaskSignals()
