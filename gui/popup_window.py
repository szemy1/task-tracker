from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QTextEdit
)
from PySide6.QtCore import Qt
from gui.style import get_theme_style
from PySide6.QtCore import QSettings
class SuggestionPopup(QDialog):
    def __init__(self, app_name, on_accept, on_reject):
        super().__init__()
        self.setWindowTitle("Feladatjavaslat")
        self.setModal(True)
        
        theme = QSettings().value("theme", "dark")
        self.setStyleSheet(get_theme_style(theme))

        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.Popup)

        self.on_accept = on_accept
        self.on_reject = on_reject

        layout = QVBoxLayout()

        info_label = QLabel(f"Úgy tűnik, a(z) „{app_name}” munkához kapcsolódik.\nAdd meg a feladat részleteit:")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        self.title_input = QLineEdit(f"Munka: {app_name}")
        layout.addWidget(QLabel("Feladat címe:"))
        layout.addWidget(self.title_input)

        self.description_input = QTextEdit()
        layout.addWidget(QLabel("Leírás:"))
        layout.addWidget(self.description_input)

        button_layout = QHBoxLayout()

        accept_button = QPushButton("Indítás")
        accept_button.clicked.connect(self.handle_accept)
        button_layout.addWidget(accept_button)

        reject_button = QPushButton("Mégsem")
        reject_button.clicked.connect(self.handle_reject)
        button_layout.addWidget(reject_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.activateWindow()
        self.raise_()

    def handle_accept(self):
        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()
        if title and self.on_accept:
            self.on_accept(title, description)
            self.accept()

    def handle_reject(self):
        if self.on_reject:
            self.on_reject()
        self.reject()
