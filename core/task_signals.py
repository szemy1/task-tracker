# core/task_signals.py

from PySide6.QtCore import Signal, QObject

class TaskSignals(QObject):
    task_started = Signal(object)
    task_stopped = Signal(object)  # itt adjuk hozzá az object paramétert!

task_signals = TaskSignals()
