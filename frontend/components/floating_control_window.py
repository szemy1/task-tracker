from PySide6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox,
    QInputDialog, QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt, QTimer, QSettings, QPoint
from PySide6.QtGui import QGuiApplication
import subprocess
import sys
import platform

class FloatingControlWindow(QDialog):
    def __init__(self, timer_manager, bring_main_window_callback, api_client):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setFixedSize(280, 200)
        self.setWindowTitle("⏱️ Időmérés")

        self.timer_manager = timer_manager
        self.bring_main_window_callback = bring_main_window_callback
        self.api_client = api_client
        self.drag_position = None
        self.is_running = False
        self.current_task_id = None
        self.suggest_enabled = True
        self.suggest_blacklist = {}
        self.known_titles = ["chrome", "Visual Studio", "pycharm", "excel"]

        self.layout = QVBoxLayout()

        self.task_selector = QComboBox()
        self.task_selector.currentIndexChanged.connect(self.select_task)
        self.layout.addWidget(self.task_selector)

        self.info_label = QLabel("Nincs aktív feladat")
        self.time_label = QLabel("00:00:00")
        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.time_label)

        button_layout = QHBoxLayout()
        self.toggle_button = QPushButton("▶️ Start")
        self.toggle_button.clicked.connect(self.toggle_timer)
        self.main_button = QPushButton("⬆️ Főablak")
        self.main_button.clicked.connect(self.bring_main_window_callback)
        button_layout.addWidget(self.toggle_button)
        button_layout.addWidget(self.main_button)
        self.layout.addLayout(button_layout)

        self.suggest_checkbox = QCheckBox("Ablak alapú javaslatok")
        self.suggest_checkbox.setChecked(True)
        self.suggest_checkbox.stateChanged.connect(self.toggle_suggest_enabled)
        self.layout.addWidget(self.suggest_checkbox)

        self.setLayout(self.layout)

        self.ui_timer = QTimer(self)
        self.ui_timer.timeout.connect(self.update_display)
        self.ui_timer.start(1000)

        self.suggest_timer = QTimer(self)
        self.suggest_timer.timeout.connect(self.check_active_window_title)
        self.suggest_timer.start(5000)  # 5 mp

        settings = QSettings("TimeTracker", "FloatingControl")
        pos = settings.value("window_position", None)
        if isinstance(pos, QPoint):
            self.move(pos)
        else:
            screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
            x = screen_geometry.width() - self.width() - 20
            y = screen_geometry.height() - self.height() - 40
            self.move(x, y)

    def toggle_suggest_enabled(self, state):
        self.suggest_enabled = bool(state)

    def check_active_window_title(self):
        if not self.suggest_enabled or self.is_running:
            return

        title = self.get_active_window_title()
        if not title:
            return

        lowered = title.lower()
        if lowered in self.suggest_blacklist:
            return

        for keyword in self.known_titles:
            if keyword.lower() in lowered:
                reply = QMessageBox.question(
                    self,
                    "Javaslat",
                    f"A(z) '{title}' ablak aktív. Elindítasz egy új feladatot?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.task_selector.setCurrentIndex(0)
                    self.toggle_timer()
                else:
                    self.suggest_blacklist[lowered] = True
                break

    def get_active_window_title(self):
        try:
            if platform.system() == "Windows":
                import ctypes
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                return buff.value
        except Exception as e:
            print(f"[HIBA] Aktív ablak lekérése: {e}")
        return None

    def update_task_list(self, tasks: list):
        self.task_selector.blockSignals(True)
        self.task_selector.clear()
        self.task_selector.addItem("\U0001f195 Új feladat létrehozása", None)
        for task in tasks:
            label = f"{task.get('name') or task.get('title', 'Ismeretlen')} ({task['id']})"
            self.task_selector.addItem(label, task['id'])
        self.task_selector.setCurrentIndex(0)
        self.current_task_id = None
        self.task_selector.blockSignals(False)

    def select_task(self, index):
        task_id = self.task_selector.itemData(index)
        self.current_task_id = task_id

    def toggle_timer(self):
        if self.is_running:
            self.timer_manager.stop_task()
            confirm = QMessageBox.question(
                self, "Feladat lezárása", "Elkészült a feladat?", QMessageBox.Yes | QMessageBox.No
            )
            try:
                if self.current_task_id:
                    if confirm == QMessageBox.Yes:
                        self.api_client.stop_task(self.current_task_id)
                    else:
                        self.api_client.update_task(self.current_task_id, status="hold")
            except Exception as e:
                print(f"[HIBA] Stop API hívás sikertelen: {e}")
            self.toggle_button.setText("▶️ Start")
            self.is_running = False
            self.current_task_id = None
            self.task_selector.setCurrentIndex(0)
            self.update_display()
            return

        else:
            try:
                if not self.current_task_id:
                    title, ok1 = QInputDialog.getText(self, "Új feladat", "Add meg a feladat nevét:")
                    if not ok1 or not title.strip(): return
                    desc, ok2 = QInputDialog.getMultiLineText(self, "Leírás", "Jegyzet vagy részletek:")
                    if not ok2: return
                    new_task = self.api_client.create_task(title, desc)
                    self.current_task_id = new_task["id"]
                    if hasattr(self, "refresh_task_list_callback"):
                        self.refresh_task_list_callback()
                    self.update_task_list(self.api_client.get_tasks())
                    for i in range(self.task_selector.count()):
                        if self.task_selector.itemData(i) == self.current_task_id:
                            self.task_selector.setCurrentIndex(i)
                            break
                self.api_client.start_task(self.current_task_id)
                self.timer_manager.start_task(self.current_task_id)
                self.toggle_button.setText("⏸️ Stop")
                self.is_running = True
            except Exception as e:
                print(f"[HIBA] Start API hívás sikertelen: {e}")
                return
        self.update_display()

    def update_display(self):
        task_info = self.timer_manager.get_active_task()
        if task_info:
            self.info_label.setText(f"Feladat: {task_info['task_id']}")
            self.time_label.setText(task_info['elapsed'])
        else:
            self.info_label.setText("Nincs aktív feladat")
            self.time_label.setText("00:00:00")

    def closeEvent(self, event):
        settings = QSettings("TimeTracker", "FloatingControl")
        settings.setValue("window_position", self.pos())
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
