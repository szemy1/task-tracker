from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox,
    QSystemTrayIcon, QMenu, QCheckBox
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QEvent, QTimer
import os, sys

from ..services.api_client import APIClient
from .new_task_dialog import NewTaskDialog
from .edit_task_dialog import EditTaskDialog
from .log_window import LogWindow
from .floating_control_window import FloatingControlWindow
from ..core.task_timer_manager import TaskTimerManager
from frontend.core.suggestion_settings import suggestion_settings
from frontend.components.window_title_watcher import WindowTitleWatcher
from backend.core.task_storage import task_storage


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.task_timer = TaskTimerManager()

        self.init_ui()
        self.load_tasks()

        all_tasks = self.api_client.get_tasks()
        task_storage.set_tasks(all_tasks)


        self.floating_control = FloatingControlWindow(
            timer_manager=self.task_timer,
            bring_main_window_callback=self.bring_to_front,
            api_client=self.api_client
        )
        self.floating_control.show()
        self.floating_control.refresh_task_list_callback = self.load_tasks
        self.load_tasks()

        self.setup_tray_icon()

        if suggestion_settings.is_enabled():
            self.window_watcher = WindowTitleWatcher(
                api_client=self.api_client,
                task_timer=self.task_timer,
                floating_control=self.floating_control  # ✅ fontos!
            )
            



    def init_ui(self):
        self.setWindowTitle("TimeTracker GUI")
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.task_list_widget = QListWidget()
        layout.addWidget(self.task_list_widget)

        refresh_button = QPushButton("Feladatok frissítése")
        refresh_button.clicked.connect(self.load_tasks)
        layout.addWidget(refresh_button)

        add_task_button = QPushButton("Új feladat hozzáadása")
        add_task_button.clicked.connect(self.open_new_task_dialog)
        layout.addWidget(add_task_button)

        delete_task_button = QPushButton("Kiválasztott feladat törlése")
        delete_task_button.clicked.connect(self.delete_selected_task)
        layout.addWidget(delete_task_button)

        log_button = QPushButton("Backend Logok megjelenítése")
        log_button.clicked.connect(self.open_log_window)
        layout.addWidget(log_button)

        # ✅ Csak egy checkbox
        self.suggestion_checkbox = QCheckBox("🧠 Ablak alapú ajánlás")
        self.suggestion_checkbox.setChecked(True)
        self.suggestion_checkbox.stateChanged.connect(
            lambda state: setattr(suggestion_settings, "_enabled", state == Qt.Checked)
        )
        layout.addWidget(self.suggestion_checkbox)

        self.task_list_widget.itemDoubleClicked.connect(self.open_edit_task_dialog)
        self.setLayout(layout)

    def setup_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = os.path.join(os.path.dirname(__file__), "..", "resources", "icon.ico")
        self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setVisible(True)

        tray_menu = QMenu()
        tray_menu.addAction(QAction("🕒 Megnyitás", self, triggered=self.bring_to_front))
        tray_menu.addAction(QAction("❌ Kilépés", self, triggered=self.quit_app))

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def bring_to_front(self):
        self.setWindowState((self.windowState() & ~Qt.WindowMinimized) | Qt.WindowActive)
        self.show()
        self.raise_()
        self.activateWindow()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.bring_to_front()

    def load_tasks(self):
        try:
            self.tasks = self.api_client.get_tasks()
            self.task_list_widget.clear()
            for task in self.tasks:
                self.task_list_widget.addItem(f"{task['id']}: {task['name']} ({task['status']})")
            if hasattr(self, "floating_control"):
                self.floating_control.update_task_list(self.tasks)
                self.floating_control.refresh_task_list_callback = self.load_tasks  # 🆕 EZ HIÁNYZOTT
        except Exception as e:
            QMessageBox.critical(self, "API hiba", f"Hiba történt: {e}")


    def open_new_task_dialog(self):
        dialog = NewTaskDialog(self.api_client, self)
        if is_running_test():
            dialog.show()
            self.current_dialog = dialog
        elif dialog.exec():
            self.load_tasks()

    def delete_selected_task(self):
        item = self.task_list_widget.currentItem()
        if not item:
            QMessageBox.warning(self, "Figyelem!", "Válassz ki egy törlendő feladatot!")
            return
        task_id = int(item.text().split(":")[0])
        if QMessageBox.question(self, "Törlés megerősítése", "Biztos?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            try:
                self.api_client.delete_task(task_id)
                QMessageBox.information(self, "Siker!", "Feladat törölve.")
                self.load_tasks()
            except Exception as e:
                QMessageBox.critical(self, "Hiba!", f"Nem sikerült: {e}")

    def open_edit_task_dialog(self, item):
        task_id = int(item.text().split(":")[0])
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if task:
            dialog = EditTaskDialog(self.api_client, task, self)
            if dialog.exec():
                self.load_tasks()

    def open_log_window(self):
        self.log_window = LogWindow()
        self.log_window.show()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange and self.isMinimized():
            QTimer.singleShot(0, self.hide)
        super().changeEvent(event)

    def closeEvent(self, event):
        if hasattr(self, 'floating_control'):
            self.floating_control.close()
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        event.accept()

    def quit_app(self):
        if hasattr(self, 'floating_control'):
            self.floating_control.close()
        QApplication.quit()


def is_running_test():
    return "pytest" in sys.modules
