from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from gui.style import modern_style

class PopupWindow(QDialog):
    def __init__(self, app_name, on_accept):
        super().__init__()
        self.setWindowTitle("Feladatjavaslat")
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        label = QLabel(f"Szeretnél feladatot indítani erre?\n\n{app_name}")
        layout.addWidget(label)

        accept_button = QPushButton("Feladat indítása")
        accept_button.clicked.connect(lambda: (on_accept(app_name), self.accept()))
        layout.addWidget(accept_button)

        decline_button = QPushButton("Nem, köszönöm")
        decline_button.clicked.connect(self.reject)
        layout.addWidget(decline_button)

        self.setLayout(layout)




class SuggestionPopup(QDialog):
    def __init__(self, suggestion_text, on_accept, on_reject):
        super().__init__()
        self.setWindowTitle("Feladatjavaslat")
        self.setModal(True)

        layout = QVBoxLayout()

        label = QLabel(suggestion_text)
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
