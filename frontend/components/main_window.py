from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox,
    QSystemTrayIcon, QMenu
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QEvent, QTimer
from ..services.api_client import APIClient
from .new_task_dialog import NewTaskDialog
from .edit_task_dialog import EditTaskDialog
from .log_window import LogWindow
from .floating_control_window import FloatingControlWindow
from ..core.task_timer_manager import TaskTimerManager
import sys
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.task_timer = TaskTimerManager()

        self.init_ui()
        self.setup_tray_icon()

        self.load_tasks()

        self.floating_control = FloatingControlWindow(
            timer_manager=self.task_timer,
            bring_main_window_callback=self.bring_to_front,
            api_client=self.api_client
        )
        self.floating_control.show()

        self.setup_tray_icon()

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

        self.task_list_widget.itemDoubleClicked.connect(self.open_edit_task_dialog)
        self.setLayout(layout)

    def setup_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = os.path.abspath("frontend/resources/icon.ico")  # vagy más relatív/abszolút út
        self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setToolTip("TimeTracker háttérben fut")
        
        tray_menu = QMenu()
        open_action = QAction("🕒 Megnyitás", self)
        open_action.triggered.connect(self.bring_to_front)
        tray_menu.addAction(open_action)

        exit_action = QAction("❌ Kilépés", self)
        exit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()


    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Bal klikk
            self.bring_to_front()

    def bring_to_front(self):
        self.setWindowState((self.windowState() & ~Qt.WindowMinimized) | Qt.WindowActive)
        self.show()
        self.raise_()
        self.activateWindow()

    def load_tasks(self):
        try:
            self.tasks = self.api_client.get_tasks()
            self.task_list_widget.clear()
            for task in self.tasks:
                self.task_list_widget.addItem(f"{task['id']}: {task['name']} ({task['status']})")
            if hasattr(self, "floating_control"):
                self.floating_control.update_task_list(self.tasks)
        except Exception as e:
            QMessageBox.critical(self, "API hiba", f"Hiba történt: {e}")

    def open_new_task_dialog(self):
        dialog = NewTaskDialog(self.api_client, self)
        if is_running_test():
            dialog.show()
            self.current_dialog = dialog
        else:
            if dialog.exec():
                self.load_tasks()

    def delete_selected_task(self):
        selected_item = self.task_list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Figyelem!", "Válassz ki egy törlendő feladatot!")
            return

        task_id = int(selected_item.text().split(":")[0])
        reply = QMessageBox.question(self, "Törlés megerősítése",
                                     "Biztosan törölni szeretnéd ezt a feladatot?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.api_client.delete_task(task_id)
                QMessageBox.information(self, "Siker!", "Feladat sikeresen törölve!")
                self.load_tasks()
            except Exception as e:
                QMessageBox.critical(self, "Hiba!", f"Feladat törlése nem sikerült: {e}")

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
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                QTimer.singleShot(0, self.hide)  # késleltetett hide, hogy ne villanjon fel újra
        super().changeEvent(event)


    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show_from_tray()

    def show_from_tray(self):
        self.show()
        self.setWindowState(Qt.WindowNoState)
        self.raise_()
        self.activateWindow()


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
