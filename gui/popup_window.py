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
    def __init__(self, app_name, on_accept):
        super().__init__()
        self.setWindowTitle("Feladatjavaslat")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.resize(300, 100)

        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel(f"Szeretnél új feladatot indítani?\n{app_name}")
        label.setAlignment(Qt.AlignCenter)

        accept_button = QPushButton("Igen")
        accept_button.clicked.connect(lambda: (on_accept(app_name), self.accept()))

        reject_button = QPushButton("Nem")
        reject_button.clicked.connect(self.reject)

        layout.addWidget(label)
        layout.addWidget(accept_button)
        layout.addWidget(reject_button)