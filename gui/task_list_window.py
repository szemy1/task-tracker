from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QPushButton, QHeaderView
)
from PySide6.QtCore import Qt
from gui.task_log_window import TaskLogWindow
from gui.style import modern_style
from PySide6.QtWidgets import QHBoxLayout, QPushButton

class TaskListWindow(QDialog):
    def __init__(self, tasks):
        super().__init__()
        self.setWindowTitle("📋 Feladatlista")
        self.resize(800, 450)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.tasks = tasks
        self.setStyleSheet(modern_style)

        layout = QVBoxLayout()
        self.setLayout(layout)

        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignRight)

        close_button = QPushButton("✖")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("border: none; font-size: 16px;")
        close_button.clicked.connect(self.close)

        top_bar.addWidget(close_button)
        layout.addLayout(top_bar)

        header_label = QLabel("🗂️ Feladatok áttekintése")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header_label)

        if not tasks:
            no_task_label = QLabel("ℹ️ Nincs még egyetlen feladat sem.")
            no_task_label.setAlignment(Qt.AlignCenter)
            no_task_label.setStyleSheet("font-size: 16px; margin-top: 20px;")
            layout.addWidget(no_task_label)
            return

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["📌 Cím", "🟢 Kezdés", "🔴 Befejezés", "⏳ Időtartam"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setRowCount(len(tasks))
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #3c3f41;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #4a90e2;
                color: #ffffff;
                padding: 8px;
                border-radius: 8px;
            }
            QTableWidget::item {
                padding: 6px;
            }
        """)

        for row, task in enumerate(tasks):
            self.table.setItem(row, 0, QTableWidgetItem(task.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(task.start_time or "–")))
            self.table.setItem(row, 2, QTableWidgetItem(str(task.end_time or "–")))
            duration = task.get_duration()
            self.table.setItem(row, 3, QTableWidgetItem(str(duration or "–")))

        self.table.cellDoubleClicked.connect(self.open_log_window)
        layout.addWidget(self.table)

        close_button = QPushButton("❌ Bezárás")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

    def open_log_window(self, row, _column):
        if 0 <= row < len(self.tasks):
            task = self.tasks[row]
            dialog = TaskLogWindow(task)
            dialog.exec()
