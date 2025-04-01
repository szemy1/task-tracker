from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QInputDialog, QLineEdit
from PySide6.QtCore import Qt, QDateTime


class SuggestTaskPopup(QDialog):
    def __init__(self, api_client, task_timer, window_title, floating_control=None, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowTitle("🕵️ Task javaslat")
        self.api_client = api_client
        self.task_timer = task_timer
        self.window_title = window_title
        self.floating_control = floating_control  # 👈 új argumentum

        suggested_title = f"{window_title} ({QDateTime.currentDateTime().toString('hh:mm')})"

        self.layout = QVBoxLayout()
        self.label = QLabel(f"Felismert ablak: <b>{window_title}</b><br>Elindítasz egy új feladatot?")
        self.layout.addWidget(self.label)

        self.layout.addWidget(QLabel("Feladat neve:"))
        self.title_input = QLineEdit(suggested_title)
        self.layout.addWidget(self.title_input)

        self.yes_button = QPushButton("✅ Igen, indítsd")
        self.yes_button.clicked.connect(self.accept)
        self.layout.addWidget(self.yes_button)

        self.no_button = QPushButton("❌ Nem most")
        self.no_button.clicked.connect(self.reject)
        self.layout.addWidget(self.no_button)

        self.setLayout(self.layout)

    def show_in_front_of_active_window(self):
        self.raise_()
        self.activateWindow()
        self.show()
        self.exec()

    def create_and_start_task(self, title, desc):
        try:
            task = self.api_client.create_task(title, desc)
            self.api_client.start_task(task["id"])
            self.task_timer.start_task(task["id"])
            return task
        except Exception as e:
            print(f"[HIBA] Task létrehozás sikertelen: {e}")
            return None

    def accept(self):
        title = self.title_input.text()
        desc, ok = QInputDialog.getMultiLineText(
            self, "Feladat leírása", "Jegyzet vagy részletek:"
        )
        if not ok:
            super().reject()
            return

        task = self.create_and_start_task(title, desc)
        if task:
            if self.floating_control:
                self.floating_control.update_after_external_start(task["id"])

        super().accept()

