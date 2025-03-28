# core/task_signals.py
from PySide6.QtCore import Signal, QObject

class TaskSignals(QObject):
    task_started = Signal(object)  # Task objektumot vár
    task_stopped = Signal(object)  # Task objektumot vár

task_signals = TaskSignals()

