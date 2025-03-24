from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QWidget
from PySide6.QtCore import Qt, QTimer, QSettings, QPoint
import datetime
import json
from gui.note_editor_dialog import NoteEditorDialog



class FloatingWidget(QWidget):
    def __init__(self, task_manager, start_task_callback, parent=None):
        super().__init__(parent)
        self.task_manager = task_manager
        self.start_task_callback = start_task_callback
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

        with open("config/settings.json", "r", encoding="utf-8") as f:
            self.settings = json.load(f)


        self.restore_position()

    def toggle_task(self):
        task = self.task_manager.get_active_task()
        if task:
            self.task_manager.stop_current_task()
            self.button.setText("Start")
            # Jegyzet ablak nyitása is jöhet ide, ha szeretnéd
            dialog = NoteEditorDialog(task)
            dialog.exec()
        else:
            dialog = TaskDetailsDialog()
            if dialog.exec() == QDialog.Accepted:
                title, description = dialog.get_details()
                self.start_task_callback(title, description)
                self.button.setText("Stop")



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
        self.settings["pos"] = [self.pos().x(), self.pos().y()]
        with open("config/settings.json", "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

        super().closeEvent(event)

    def restore_position(self):
        pos = self.settings.get("pos")
        if isinstance(pos, QPoint):
            self.move(pos)

class TaskDetailsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gyors feladat indítása")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Feladat címe:"))
        self.title_input = QLineEdit("Gyors feladat")
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Leírás:"))
        self.desc_input = QTextEdit()
        layout.addWidget(self.desc_input)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Indítás")
        self.cancel_button = QPushButton("Mégsem")
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.start_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_details(self):
        return self.title_input.text().strip(), self.desc_input.toPlainText().strip()
