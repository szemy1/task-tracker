from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout
)
from PySide6.QtCore import Qt
from gui.task_timeline_window import TaskTimelineWindow
from gui.style import modern_style
from gui.note_editor_dialog import NoteEditorDialog
from core.task_manager import TaskManager


class TaskLogWindow(QDialog):
    def __init__(self, task, task_manager: TaskManager):
        super().__init__()
        self.task = task
        self.task_manager = task_manager

        self.setWindowTitle(f"📃 Napló: {task.title}")
        self.resize(600, 500)
        self.setStyleSheet(modern_style)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Top bar - bezáró gomb
        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignRight)

        close_button = QPushButton("✖")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("border: none; font-size: 16px;")
        close_button.clicked.connect(self.close)

        top_bar.addWidget(close_button)
        layout.addLayout(top_bar)

        # Feladat cím
        self.label = QLabel(f"📍 Feladat: {task.title}")
        self.label.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(self.label)

        # Napló lista
        self.log_list = QListWidget()
        self.refresh_logs()
        layout.addWidget(self.log_list)

        # Gombok
        button_layout = QHBoxLayout()

        timeline_button = QPushButton("📅 Idővonal megnyitása")
        timeline_button.clicked.connect(self.open_timeline)
        button_layout.addWidget(timeline_button)

        note_button = QPushButton("📝 Jegyzet megnyitása")
        note_button.clicked.connect(self.open_note_editor)
        button_layout.addWidget(note_button)

        layout.addLayout(button_layout)

    def refresh_logs(self):
        self.log_list.clear()
        for timestamp, message in self.task.logs:
            item = QListWidgetItem(f"[{timestamp.strftime('%H:%M:%S')}] {message}")
            self.log_list.addItem(item)

    def open_timeline(self):
        timeline_window = TaskTimelineWindow(self.task, on_new_task_callback=self.create_task_from_logs)
        timeline_window.exec()

    def create_task_from_logs(self, title, description, logs):
        from core.task_manager import Task
        new_task = Task(title=title, description=description)
        new_task.start_time = logs[0][0] if logs else None
        new_task.end_time = logs[-1][0] if logs else None
        new_task.logs = logs
        self.task_manager.tasks.append(new_task)
        self.task_manager.save()

    def open_note_editor(self):
        # Jegyzet szerkesztő megnyitása – automatikus betöltéssel
        editor = NoteEditorDialog(self.task)
        editor.exec()
