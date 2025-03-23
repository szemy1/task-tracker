# gui/close_task_dialog.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel

class CloseTaskDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Feladat lezárása – dokumentáció")
        self.resize(500, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Írd le, mit végeztél el ezzel a feladattal kapcsolatban:"))

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Pl.: Bug javítva, fájl frissítve, ügyfél visszajelzést kapott...")
        layout.addWidget(self.notes_input)

        self.save_button = QPushButton("Mentés és lezárás")
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

    def get_notes(self):
        return self.notes_input.toPlainText().strip()
