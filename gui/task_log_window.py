# gui/task_log_window.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from gui.task_timeline_window import TaskTimelineWindow
from core.task_manager import Task
from core.tag_styles import get_tag_style  # 🔥 új: címke-stílus import

class TaskLogWindow(QDialog):
    def __init__(self, task):
        super().__init__()
        self.setWindowTitle(f"Napló: {task.title}")
        self.resize(600, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.task = task

        layout.addWidget(QLabel(f"Leírás: {task.description}"))
        layout.addWidget(QLabel(f"Kezdés: {task.start_time}"))
        layout.addWidget(QLabel(f"Befejezés: {task.end_time}"))
        layout.addWidget(QLabel("Események:"))

        self.log_list = QListWidget()
        layout.addWidget(self.log_list)

        for timestamp, message in task.logs:
            display_text = f"[{timestamp}] {message}"
            item = QListWidgetItem(display_text)

            # 🔍 Ha van címke, akkor színezzük és emoji-t is adunk hozzá
            if "Típus:" in message:
                tag = message.split("Típus:")[-1].strip()
                style = get_tag_style(tag)
                item.setForeground(QColor(style["color"]))
                item.setText(f"[{timestamp}] {style['emoji']} {message}")

            self.log_list.addItem(item)

        self.log_list.setCurrentRow(-1)

        # 🕒 Timeline gomb
        self.timeline_button = QPushButton("Megtekintés idővonalon")
        self.timeline_button.clicked.connect(self.open_timeline)
        layout.addWidget(self.timeline_button)

    def open_timeline(self):
        timeline_window = TaskTimelineWindow(self.task, on_new_task_callback=self.create_task_from_logs)
        timeline_window.exec()

    def create_task_from_logs(self, title, description, logs):
        from core.task_manager import Task
        from gui.main_window import MainWindow  # ⚠️ fontos a circular import miatt

        new_task = Task(title, description)
        for ts, msg in logs:
            new_task.logs.append((ts, msg))
        new_task.start_time = logs[0][0] if logs else None
        new_task.end_time = logs[-1][0] if logs else None
        new_task.log_event("Feladat létrehozva idővonal alapján")

        MainWindow.instance.task_manager.tasks.append(new_task)
        MainWindow.instance.task_manager.save()
