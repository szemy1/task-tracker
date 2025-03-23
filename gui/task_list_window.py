from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
)
from gui.task_log_window import TaskLogWindow

class TaskListWindow(QDialog):
    def __init__(self, tasks):
        super().__init__()
        self.setWindowTitle("Feladatlista")
        self.resize(700, 400)
        self.tasks = tasks

        layout = QVBoxLayout()
        self.setLayout(layout)

        if not tasks:
            layout.addWidget(QLabel("Nincs még egyetlen feladat sem."))
            return

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Cím", "Kezdés", "Befejezés", "Időtartam"])
        self.table.setRowCount(len(tasks))

        for row, task in enumerate(tasks):
            self.table.setItem(row, 0, QTableWidgetItem(task.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(task.start_time or "–")))
            self.table.setItem(row, 2, QTableWidgetItem(str(task.end_time or "–")))
            duration = task.get_duration()
            self.table.setItem(row, 3, QTableWidgetItem(str(duration or "–")))

        self.table.cellDoubleClicked.connect(self.open_log_window)
        layout.addWidget(self.table)

    def open_log_window(self, row, _column):
        if 0 <= row < len(self.tasks):
            task = self.tasks[row]
            dialog = TaskLogWindow(task)
            dialog.exec()
