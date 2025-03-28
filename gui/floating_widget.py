from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QWidget
from PySide6.QtCore import Qt, QTimer, QSettings, QPoint
import datetime
import json
import sys
import os
from gui.note_editor_dialog import NoteEditorDialog
from gui.style import get_theme_style
from core.task_signals import task_signals


class TaskDetailsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gyors feladat indítása")
        self.setMinimumWidth(300)
        settings = QSettings("TimeMeter", "TaskTracker")
        theme = settings.value("theme", "dark")
        self.setStyleSheet(get_theme_style(theme))

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


class FloatingWidget(QWidget):
    def __init__(self, task_manager, start_task_callback, parent=None):
        super().__init__(parent)
        self.task_manager = task_manager
        self.start_task_callback = start_task_callback
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setFixedSize(300, 120)

        # 🔧 Objektum név stílushoz
        self.setObjectName("FloatingWidget")

        # 🎨 Téma alkalmazása
        settings_store = QSettings("TimeMeter", "TaskTracker")
        theme = settings_store.value("theme", "dark").lower()
        self.setStyleSheet(get_theme_style(theme, is_floating=True))

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


        # Beállítások betöltése
        try:
            with open(self.resource_path("config/settings.json"), "r", encoding="utf-8") as f:

                self.settings = json.load(f)
        except Exception:
            self.settings = {}

        self.restore_position()

        # 🔄 Globális task jelek figyelése
        task_signals.task_started.connect(self.on_external_task_started)
        task_signals.task_stopped.connect(self.on_external_task_stopped)
    
    
    def resource_path(self, relative_path):
        """Adott fájl elérési útja – működik PyInstaller alatt is."""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)



    def toggle_task(self):
        task = self.task_manager.get_active_task()

        # Ha van aktív task, akkor állítsuk le
        if task and task.is_active:
            self.task_manager.stop_current_task()
            task_signals.task_stopped.emit(task)
            dialog = NoteEditorDialog(task)
            dialog.exec()
            self.button.setText("Start")
        else:
            # Új task indítása dialoggal
            dialog = TaskDetailsDialog()
            if dialog.exec() == QDialog.Accepted:
                title, description = dialog.get_details()
                self.task_manager.start_task(title, description)
                new_task = self.task_manager.get_active_task()
                task_signals.task_started.emit(new_task)
                self.button.setText("Stop")

        self.update_ui()


    def clear_current_task(self):
        self._current_task = None



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

    def restore_position(self):
        if "floating_widget_pos" in self.settings:
            pos = self.settings["floating_widget_pos"]
            self.move(QPoint(pos[0], pos[1]))

    def closeEvent(self, event):
        self.settings["floating_widget_pos"] = [self.x(), self.y()]
        with open(self.resource_path("config/settings.json"), "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=2)
        event.accept()

    def mousePressEvent(self, event):
        self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()

    def on_external_task_started(self, task_data):
        self.update_ui()
        self.show()

    def on_external_task_stopped(self):
        self.update_ui()