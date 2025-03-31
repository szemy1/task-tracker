from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox
from ..services.api_client import APIClient
from .new_task_dialog import NewTaskDialog
from .edit_task_dialog import EditTaskDialog
from .log_window import LogWindow
import sys




class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.init_ui()
        self.load_tasks()

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

        # Itt kell lennie a log-ablak gombjának:
        log_button = QPushButton("Backend Logok megjelenítése")
        log_button.clicked.connect(self.open_log_window)
        layout.addWidget(log_button)

        self.task_list_widget.itemDoubleClicked.connect(self.open_edit_task_dialog)

        self.setLayout(layout)

    def load_tasks(self):
        try:
            self.tasks = self.api_client.get_tasks()
            self.task_list_widget.clear()
            for task in self.tasks:
                self.task_list_widget.addItem(f"{task['id']}: {task['name']} ({task['status']})")
        except Exception as e:
            QMessageBox.critical(self, "API hiba", f"Hiba történt: {e}")


    def open_new_task_dialog(self):
        dialog = NewTaskDialog(self.api_client, self)
        if is_running_test():
            dialog.show()
            self.current_dialog = dialog  # teszteléshez elérhetővé tesszük
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

        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


def is_running_test():
    return "pytest" in sys.modules