import os
import json
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import Qt  # ← Ezt add hozzá!
from gui.style import modern_style
from PySide6.QtWidgets import QCheckBox, QFileDialog, QLabel
from PySide6.QtCore import QSettings
import os


CONFIG_PATH = "config/settings.json"

DEFAULT_SETTINGS = {
    "auto_archive_days": 7,
    "storage_path": "./data",
    "inactivity_limit_minutes": 10,
    "theme": "light"
}



class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beállítások")
        self.resize(400, 250)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.settings = self.load_settings()
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

        self.archive_days_input = QLineEdit(str(self.settings["auto_archive_days"]))
        self.path_input = QLineEdit(self.settings["storage_path"])
        self.inactivity_input = QLineEdit(str(self.settings["inactivity_limit_minutes"]))
        self.theme_input = QLineEdit(self.settings.get("theme", "light"))

        path_button = QPushButton("Tallózás...")
        path_button.clicked.connect(self.browse_folder)

        save_button = QPushButton("Mentés")
        save_button.clicked.connect(self.save)

        layout.addWidget(QLabel("Automatikus archiválás naponta (pl. 7):"))
        layout.addWidget(self.archive_days_input)
        layout.addWidget(QLabel("Mentési útvonal:"))
        layout.addWidget(self.path_input)
        layout.addWidget(path_button)
        layout.addWidget(QLabel("Inaktivitási limit (perc):"))
        layout.addWidget(self.inactivity_input)
        layout.addWidget(QLabel("Téma (light / dark):"))         # ← a hibás sor
        layout.addWidget(self.theme_input)                       # ← új mező


        self.setLayout(layout)  # ← FONTOS! csak ezután lesz self.layout() működőképes
        # 🔘 Lebegő ablak kapcsoló
        self.floating_checkbox = QCheckBox("Lebegő ablak megjelenítése")
        self.floating_checkbox.setChecked(self.settings.get("floating_enabled", True))
        layout.addWidget(self.floating_checkbox)

        # 🖼️ Logó kiválasztása
        self.logo_label = QLabel("Logó: nincs kiválasztva")
        self.logo_path = self.settings.get("logo_path", "")
        if self.logo_path:
            self.logo_label.setText(f"Logó: {os.path.basename(self.logo_path)}")
        layout.addWidget(self.logo_label)

        self.logo_button = QPushButton("Logó kiválasztása")
        self.logo_button.clicked.connect(self.choose_logo)
        layout.addWidget(self.logo_button)
        layout.addWidget(save_button)



    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Válassz mappát")
        if folder:
            self.path_input.setText(folder)

    def load_settings(self):
        if not os.path.exists(CONFIG_PATH):
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, "w") as f:
                json.dump(DEFAULT_SETTINGS, f, indent=4)
            return DEFAULT_SETTINGS.copy()

        with open(CONFIG_PATH, "r") as f:
            return json.load(f)


    def choose_logo(self):
        file, _ = QFileDialog.getOpenFileName(self, "Logó kiválasztása", "", "Képek (*.png *.ico *.jpg)")
        if file:
            self.logo_path = file
            self.logo_label.setText(f"Logó: {os.path.basename(file)}")

    def save(self):
        try:
            new_settings = {
                "auto_archive_days": int(self.archive_days_input.text()),
                "storage_path": self.path_input.text(),
                "theme": self.theme_input.text().strip(),
                "floating_enabled": self.floating_checkbox.isChecked(),
                "logo_path": self.logo_path or "",
                "inactivity_limit_minutes": int(self.inactivity_input.text())
            }

            with open(CONFIG_PATH, "w") as f:
                json.dump(new_settings, f, indent=4)

            QMessageBox.information(self, "Mentve", "Beállítások elmentve.")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Hibás beviteli érték: {e}")

