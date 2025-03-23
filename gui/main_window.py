from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, 
    QLineEdit, QTextEdit, QMessageBox, QDialog, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt, QPoint
from core.task_manager import TaskManager
from gui.task_list_window import TaskListWindow
from gui.close_task_dialog import CloseTaskDialog
from gui.settings_window import SettingsWindow
from gui.stats_window import StatsWindow
from gui.analysis_window import AnalysisWindow
from gui.dashboard_window import DashboardWindow
from core.predictor import predict_duration
from gui.popup_window import PopupWindow
from core.app_logger import AppLogger
from gui.popup_window import SuggestionPopup
# gui/main_window.py
from core.activity_notifier import ActivityNotifier


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setMinimumSize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        # Kilépés gomb hozzáadása (felül)
        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignRight)

        close_button = QPushButton("✖")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("border: none; font-size: 16px;")
        close_button.clicked.connect(self.close)

        top_bar.addWidget(close_button)
        self.layout.addLayout(top_bar)

        # Ablak mozgatásához
        self.old_position = QPoint()
        self.task_manager = TaskManager()

        # Cím
        title_label = QLabel("🚀 Task Tracker")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18pt;")
        self.layout.addWidget(title_label)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Feladat címe")
        self.layout.addWidget(self.title_input)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Feladat leírása")
        self.layout.addWidget(self.description_input)

        self.start_button = QPushButton("▶️ Feladat indítása")
        self.start_button.clicked.connect(self.start_task)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("⏹️ Feladat leállítása")
        self.stop_button.clicked.connect(self.stop_task)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button)

        self.status_label = QLabel("🟡 Nincs aktív feladat")
        self.layout.addWidget(self.status_label)

        # Menügombok
        buttons = [
            ("📋 Feladatlista", self.show_task_list),
            ("📊 Heti statisztika", self.show_stats),
            ("🧠 Elemzés", self.show_analysis),
            ("📈 AI Dashboard", self.show_dashboard),
            ("⚙️ Beállítások", self.open_settings),
        ]
        for text, slot in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            self.layout.addWidget(btn)
        
        self.activity_notifier = ActivityNotifier()
        self.activity_notifier.suggest_task_signal.connect(self.show_suggestion_popup)

        self.app_logger = AppLogger(self.task_manager, self.activity_notifier)
        self.app_logger.start()

        # Stílus betöltése
        self.load_styles()

    def show_suggestion_popup(self, app_name):
        self.popup = SuggestionPopup(app_name, self.start_suggested_task)
        self.popup.show()

    def start_suggested_task(self, app_name):
        self.title_input.setText(app_name)
        self.start_task()


    def show_task_suggestion(self, app_name):
        if not self.task_manager.get_active_task():
            popup = PopupWindow(app_name, self.start_suggested_task)
            popup.exec()

    def start_suggested_task(self, app_name):
        self.title_input.setText(f"Munka: {app_name}")
        self.start_task()

    def closeEvent(self, event):
        self.app_logger.stop()
        event.accept()


    def show_suggestion_popup(self, app_name):
        popup = PopupWindow(app_name, self.start_suggested_task)
        popup.exec()

    def start_suggested_task(self, app_name):
        self.title_input.setText(app_name)
        self.start_task()

    def load_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #282c34;
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 11pt;
            }
            QPushButton {
                background-color: #61afef;
                border-radius: 8px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #5090c4;
            }
            QLineEdit, QTextEdit {
                background-color: #3c4048;
                border-radius: 6px;
                padding: 6px;
            }
        """)

    # Ablak mozgatása egérrel
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_position
        self.move(self.pos() + delta)
        self.old_position = event.globalPosition().toPoint()

    def show_dashboard(self):
        dialog = DashboardWindow(self.task_manager.get_all_tasks())
        dialog.exec()

    def show_analysis(self):
        dialog = AnalysisWindow(self.task_manager.get_all_tasks())
        dialog.exec()

    def show_stats(self):
        dialog = StatsWindow(self.task_manager.get_all_tasks())
        dialog.exec()

    def open_settings(self):
        dialog = SettingsWindow()
        dialog.exec()

    def show_task_list(self):
        dialog = TaskListWindow(self.task_manager.get_all_tasks())
        dialog.exec()

    def start_task(self):
        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "⚠️ Hiba", "Kérlek adj meg egy feladatcímet!")
            return

        prediction = predict_duration(title, description, self.task_manager.get_all_tasks())
        if prediction:
            QMessageBox.information(self, "🔮 AI becslés", f"A rendszer szerint kb. {prediction} percet vesz igénybe.")

        task = self.task_manager.create_task(title, description)
        self.task_manager.start_current_task(self.activity_notifier)  # Itt adjuk át
        self.status_label.setText(f"🟢 Futó feladat: {task.title}")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)


    def stop_task(self):
        self.task_manager.stop_current_task()
        task = self.task_manager.get_active_task()
        duration = task.get_duration()
        self.status_label.setText(f"🔴 Feladat lezárva: {task.title} ({duration})")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        dialog = CloseTaskDialog()
        result = dialog.exec()

        if result == QDialog.Accepted:
            notes = dialog.get_notes()
            if notes:
                task.log_event(f"Záró megjegyzés: {notes}")

        self.task_manager.check_auto_archive(self)
