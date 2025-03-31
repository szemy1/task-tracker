from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from PySide6.QtCore import QTimer
import os

class LogWindow(QWidget):
    def __init__(self, log_file=None):
        super().__init__()
        self.log_file = log_file or os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend.log"))
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Backend logok (DEBUG)")
        self.resize(700, 400)

        layout = QVBoxLayout()

        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        layout.addWidget(self.log_text_edit)

        refresh_button = QPushButton("Frissítés")
        refresh_button.clicked.connect(self.load_logs)
        layout.addWidget(refresh_button)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.load_logs)
        self.timer.start(3000)  # Automatikus frissítés 3 másodpercenként

        self.load_logs()

    def load_logs(self):
        try:
            log_file_path = os.path.join(os.path.dirname(__file__), self.log_file)
            # Explicit Windows-kódolással olvasás (ez fogja javítani a hibát)
            with open(log_file_path, "r", encoding="cp1250") as file:
                content = file.read()
            self.log_text_edit.setPlainText(content)
            self.log_text_edit.verticalScrollBar().setValue(
                self.log_text_edit.verticalScrollBar().maximum()
            )
        except FileNotFoundError:
            self.log_text_edit.setPlainText("Nem található a logfájl.")
        except UnicodeDecodeError:
            self.log_text_edit.setPlainText("Kódolási hiba a logfájl olvasásakor.")

