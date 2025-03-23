# gui/close_task_dialog.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel
from gui.style import modern_style
from PySide6.QtWidgets import QHBoxLayout, QPushButton
from PySide6.QtCore import Qt


class CloseTaskDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Feladat lezárása – dokumentáció")
        self.resize(500, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setStyleSheet(modern_style)

        layout = QVBoxLayout()
        self.setLayout(layout)

        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignRight)

        close_button = QPushButton("✖")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("border: none; font-size: 16px;")
        close_button.clicked.connect(self.close)

        top_bar.addWidget(close_button)
        layout.addLayout(top_bar)

        layout.addWidget(QLabel("Írd le, mit végeztél el ezzel a feladattal kapcsolatban:"))

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Pl.: Bug javítva, fájl frissítve, ügyfél visszajelzést kapott...")
        layout.addWidget(self.notes_input)

        self.save_button = QPushButton("Mentés és lezárás")
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

    def get_notes(self):
        return self.notes_input.toPlainText().strip()
