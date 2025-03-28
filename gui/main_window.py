from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QMessageBox, QDialog, QHBoxLayout
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
from core.app_logger import AppLogger
from gui.popup_window import SuggestionPopup
from core.activity_notifier import ActivityNotifier
from gui.note_editor_dialog import NoteEditorDialog
from gui.floating_widget import FloatingWidget
from PySide6.QtCore import QSettings
import json
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QAction, QCursor
import os
from PySide6.QtCore import QEvent
from gui.style import get_theme_style
from core.task_signals import task_signals
from datetime import datetime
from core.task_signals import task_signals
import sys
import os


class MainWindow(QMainWindow):
    instance = None  # <<< EZ KELL
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setMinimumSize(800, 600)
        self.popup_shown = False  # Új felugró figyelő változó
        MainWindow.instance = self
        

        # __init__ elején:
        with open(self.resource_path("config/settings.json"), "r", encoding="utf-8") as f:

            self.settings = json.load(f)



        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        # Bezáró gomb
        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignRight)

        close_button = QPushButton("✖")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("border: none; font-size: 16px;")
        close_button.clicked.connect(self.close)

        top_bar.addWidget(close_button)
        self.layout.addLayout(top_bar)

        self.old_position = QPoint()
        self.task_manager = TaskManager()

        # Cím
        title_label = QLabel("🚀 Task Tracker")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18pt;")
        self.layout.addWidget(title_label)

        # Beviteli mezők
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

        # Menü gombok
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

        # Értesítési rendszer + logger
        self.activity_notifier = ActivityNotifier()
        self.activity_notifier.suggest_task_signal.connect(self.show_suggestion_popup)

        self.app_logger = AppLogger(self.task_manager, self.activity_notifier)
        self.app_logger.start()

        self.load_styles()
        # 💡 Lebegő ablak beállítás alapján
        floating = self.settings.get("floating_enabled", True)
        print(f"[DEBUG] Floating enabled setting: {floating}")
        if self.settings.get("floating_enabled", True):
            self.floating_widget = FloatingWidget(self.task_manager, self.start_task, parent=None)
            self.floating_widget.show()
        else:
            self.floating_widget = None

        self.setup_tray_icon()
        # Kilépő gomb (valódi kilépés, nem csak minimalizálás)
        exit_button = QPushButton("🛑")
        exit_button.setFixedSize(30, 30)
        exit_button.setStyleSheet("border: none; font-size: 16px;")
        exit_button.setToolTip("Kilépés az alkalmazásból")
        exit_button.clicked.connect(self.exit_app)  # <- ez hívja a valódi kilépő metódust

        top_bar.addWidget(exit_button)
        # Feladat jelzések összekapcsolása GUI frissítéshez
        task_signals.task_started.connect(self.on_task_started)
        task_signals.task_stopped.connect(self.on_task_stopped)



    def resource_path(self, relative_path):
        """Adott fájl elérési útja – működik PyInstaller alatt is."""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)


    def load_styles(self):
        theme = self.settings.get("theme", "dark").lower()
        self.setStyleSheet(get_theme_style(theme))


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.old_position
        self.move(self.pos() + delta)
        self.old_position = event.globalPosition().toPoint()

    def show_suggestion_popup(self, app_name):
        if self.popup_shown:
            return

        self.popup_shown = True

        def on_accept(title, description):
            self.popup_shown = False
            self.title_input.setText(title)
            self.description_input.setPlainText(description)
            self.start_task()

        def on_reject():
            self.popup_shown = False
            self.app_logger.dismiss_window(app_name)  # ✅ ITT hívjuk meg
            print("Feladatjavaslat elutasítva")

        popup = SuggestionPopup(app_name, on_accept, on_reject)
        popup.exec()





    def start_task(self, title=None, description=None):
        if self.task_manager.get_active_task():
            self.stop_task()

        if title is None:
            title = self.title_input.text().strip()
        if description is None:
            description = self.description_input.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "⚠️ Hiba", "Kérlek adj meg egy feladatcímet!")
            return

        prediction = predict_duration(title, description, self.task_manager.get_all_tasks())
        if prediction:
            QMessageBox.information(self, "🔮 AI becslés", f"A rendszer szerint kb. {prediction} percet vesz igénybe.")

        task = self.task_manager.create_task(title, description)
        self.task_manager.start_current_task(self.activity_notifier)

        self.status_label.setText(f"🟢 Futó feladat: {task.title}")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        # 🔁 KIEGÉSZÍTÉS: floating widget + tray viselkedés stabilizálása
        task_signals.task_started.emit(task)


        self.show()
        self.raise_()
        self.activateWindow()

        if hasattr(self, "floating_widget") and self.floating_widget:
            self.floating_widget.show()


    def start_task_from_floating(self, title=None, description=None):
        if self.task_manager.get_active_task():
            self.stop_task()

        if not title:
            title = "Gyors feladat"

        task = self.task_manager.create_task(title, description)
        self.task_manager.start_current_task(self.activity_notifier)

        self.status_label.setText(f"🟢 Futó feladat: {task.title}")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)


    def stop_task(self):
        task = self.task_manager.get_active_task()
        self.task_manager.stop_current_task()
        task_signals.task_stopped.emit(task)  # <<-- hozzáadva
        duration = task.get_duration()
        self.status_label.setText(f"🔴 Feladat lezárva: {task.title} ({duration})")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        dialog = NoteEditorDialog(task)
        if dialog.exec() == QDialog.Accepted:
            print("Jegyzet mentve.")

        self.task_manager.check_auto_archive(self)


    def show_task_list(self):
        dialog = TaskListWindow(self.task_manager)
        dialog.exec()

    def show_stats(self):
        dialog = StatsWindow(self.task_manager.get_all_tasks())
        dialog.exec()

    def show_analysis(self):
        dialog = AnalysisWindow(self.task_manager.get_all_tasks())
        dialog.exec()

    def show_dashboard(self):
        dialog = DashboardWindow(self.task_manager.get_all_tasks())
        dialog.exec()

    def open_settings(self):
        dialog = SettingsWindow()
        dialog.exec()

    def closeEvent(self, event):
        event.ignore()  # Ne zárja be az appot
        self.hide()
        if hasattr(self, "tray_icon") and self.tray_icon:
            self.tray_icon.showMessage("TimeMeter", "Az alkalmazás a tálcára lett minimalizálva.")

    def setup_tray_icon(self):
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icon.ico"))
        self.tray_icon = QSystemTrayIcon(self)
        icon = QIcon(icon_path)
        self.tray_icon.setIcon(icon)

        self.tray_menu = QMenu(self)
        self.tray_icon.setToolTip("Kattints jobb gombbal a menü megnyitásához")

        show_action = QAction("🟢 Megnyitás")
        show_action.triggered.connect(self.show_from_tray)
        self.tray_menu.addAction(show_action)

        quit_action = QAction("❌ Kilépés")
        quit_action.triggered.connect(self.exit_app)
        self.tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated) # ✅ Fontos!

        if icon.isNull():
            print("[TRAY] ❌ Ikon nincs betöltve!")
        else:
            print("[TRAY] ✅ Ikon sikeresen betöltve.")

        self.tray_icon.setVisible(True)
        self.tray_icon.show()




    def show_normal(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()
        if hasattr(self, "floating_widget") and self.floating_widget:
            self.floating_widget.show()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.raise_()
            self.activateWindow()

        print(f"[TRAY DEBUG] Aktiválva: {reason}")
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.show_from_tray()
        elif reason == QSystemTrayIcon.Context:
            print("[TRAY DEBUG] Jobb klikk (popup megjelenítés próbálkozás)")

            # Biztonságosabb, natívabb menü megjelenítés
            pos = QCursor.pos()
            action = self.tray_menu.exec(pos)
            if action:
                print(f"[TRAY DEBUG] Menü választás: {action.text()}")
            else:
                print("[TRAY DEBUG] Menü bezárva választás nélkül.")



    def show_from_tray(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()
        if hasattr(self, "floating_widget") and self.floating_widget:
            self.floating_widget.show()

    def exit_app(self):
        if self.app_logger:
            self.app_logger.stop()
            self.app_logger.join()
        if hasattr(self, "floating_widget") and self.floating_widget:
            self.floating_widget.close()
        if hasattr(self, "tray_icon"):
            self.tray_icon.hide()
        QApplication.quit()

    def on_task_started(self, task):
        self.status_label.setText(f"🟢 Futó feladat: {task.title}")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        if hasattr(self, "floating_widget") and self.floating_widget:
            self.floating_widget.update_ui()

    def on_task_stopped(self, task):
        self.status_label.setText(f"🔴 Feladat lezárva: {task.title}")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        if hasattr(self, "floating_widget") and self.floating_widget:
            self.floating_widget.update_ui()

