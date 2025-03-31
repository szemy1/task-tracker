from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QMessageBox

class EditTaskDialog(QDialog):
    def __init__(self, api_client, task, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.task = task
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Feladat szerkesztése")
        self.resize(400, 200)

        layout = QVBoxLayout()

        self.name_input = QLineEdit(self.task["name"])
        layout.addWidget(self.name_input)

        self.desc_input = QTextEdit(self.task.get("description", ""))
        layout.addWidget(self.desc_input)

        save_button = QPushButton("Mentés")
        save_button.clicked.connect(self.save_task)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_task(self):
        name = self.name_input.text().strip()
        description = self.desc_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Figyelem!", "A feladat neve kötelező!")
            return

        task_data = {
            "id": self.task["id"],
            "name": name,
            "description": description,
            "status": self.task["status"]
        }

        try:
            self.api_client.update_task(self.task["id"], task_data)
            QMessageBox.information(self, "Siker!", "Feladat sikeresen frissítve!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Hiba!", f"Feladat frissítése nem sikerült: {e}")
