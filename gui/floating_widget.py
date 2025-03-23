from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QSettings, QPoint
import datetime


class FloatingWidget(QWidget):
    def __init__(self, task_manager, parent=None):
        super().__init__(parent)
        self.task_manager = task_manager
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setFixedSize(300, 120)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
                border: 2px solid #4a90e2;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #4a90e2;
                border: none;
                padding: 5px 10px;
                border-radius: 6px;
                color: white;
            }
        """)

        self.title_label = QLabel("⏳ Nincs aktív feladat")
        self.time_label = QLabel("00:00:00")
        self.button = QPushButton("Start")

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.time_label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.button.clicked.connect(self.toggle_task)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)

        self.settings = QSettings("TimeMeter", "FloatingWidget")
        self.restore_position()

    def toggle_task(self):
        task = self.task_manager.get_active_task()
        if task:
            self.task_manager.stop_current_task()
        else:
            self.task_manager.create_task("Gyorsfeladat")
            self.task_manager.start_current_task(None)
        self.update_ui()

    def update_ui(self):
        task = self.task_manager.get_active_task()
        if task and task.is_active:
            self.title_label.setText(f"🎯 {task.title}")
            duration = datetime.datetime.now() - task.start_time
            self.time_label.setText(str(duration).split(".")[0])
            self.button.setText("Stop")
        else:
            self.title_label.setText("⏳ Nincs aktív feladat")
            self.time_label.setText("00:00:00")
            self.button.setText("Start")

    def mousePressEvent(self, event):
        self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()

    def closeEvent(self, event):
        self.settings.setValue("pos", self.pos())
        super().closeEvent(event)

    def restore_position(self):
        pos = self.settings.value("pos")
        if isinstance(pos, QPoint):
            self.move(pos)
