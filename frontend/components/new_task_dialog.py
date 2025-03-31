from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QMessageBox

class NewTaskDialog(QDialog):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Új feladat hozzáadása")
        self.resize(400, 200)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Feladat neve")
        layout.addWidget(self.name_input)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Leírás (nem kötelező)")
        layout.addWidget(self.desc_input)

        add_button = QPushButton("Hozzáadás")
        add_button.clicked.connect(self.add_task)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_task(self):
        name = self.name_input.text().strip()
        description = self.desc_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Figyelem!", "A feladat neve kötelező!")
            return

        task_data = {
            "name": name,
            "description": description,
            "status": "open"
        }

        try:
            self.api_client.create_task(task_data)
            QMessageBox.information(self, "Siker!", "Feladat sikeresen létrehozva!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Hiba!", f"Feladat létrehozása nem sikerült: {e}")

