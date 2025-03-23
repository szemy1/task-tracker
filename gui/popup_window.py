from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from gui.style import modern_style

class SuggestionPopup(QDialog):
    def __init__(self, suggestion_text, on_accept, on_reject):
        super().__init__()
        self.setWindowTitle("Feladatjavaslat")
        self.setModal(True)
        self.setStyleSheet(modern_style)

        # Itt jön a lényeg: mindig legfelülre helyezzük
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.Popup)

        layout = QVBoxLayout()

        label = QLabel(suggestion_text)
        label.setWordWrap(True)
        layout.addWidget(label)

        button_layout = QHBoxLayout()

        accept_button = QPushButton("Elfogad")
        accept_button.clicked.connect(lambda: (on_accept(), self.accept()))
        button_layout.addWidget(accept_button)

        reject_button = QPushButton("Elutasít")
        reject_button.clicked.connect(lambda: (on_reject(), self.reject()))
        button_layout.addWidget(reject_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Fókusz ráadás
        self.activateWindow()
        self.raise_()
