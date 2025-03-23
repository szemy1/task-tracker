# gui/main_window.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QMessageBox, QDialog
)
from PySide6.QtCore import Qt
from core.task_manager import TaskManager
from gui.task_list_window import TaskListWindow
from gui.close_task_dialog import CloseTaskDialog
from exports.excel_exporter import export_tasks_to_excel
from gui.task_timeline_window import TaskTimelineWindow
from gui.settings_window import SettingsWindow
from gui.stats_window import StatsWindow
from gui.analysis_window import AnalysisWindow
from gui.dashboard_window import DashboardWindow
from core.predictor import predict_duration


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Tracker")
        self.setMinimumSize(800, 600)

        self.task_manager = TaskManager()

        # Központi widget és layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()  # <<< LOKÁLIS HELYETT PÉLDÁNYVÁLTOZÓ!
        central_widget.setLayout(self.layout)

        # Feladat név
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Feladat címe")
        self.layout.addWidget(self.title_input)

        # Leírás
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Feladat leírása")
        self.layout.addWidget(self.description_input)

        # Indítás gomb
        self.start_button = QPushButton("Feladat indítása")
        self.start_button.clicked.connect(self.start_task)
        self.layout.addWidget(self.start_button)

        # Leállítás gomb
        self.stop_button = QPushButton("Feladat leállítása")
        self.stop_button.clicked.connect(self.stop_task)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button)

        # Aktuális feladat kijelző
        self.status_label = QLabel("Nincs aktív feladat")
        self.layout.addWidget(self.status_label)

        # Gomb: feladatok listázása
        self.list_button = QPushButton("Feladatlista megtekintése")
        self.list_button.clicked.connect(self.show_task_list)
        self.layout.addWidget(self.list_button)

        # Gomb: Excel export
        self.export_button = QPushButton("Excel export")
        self.export_button.clicked.connect(self.export_to_excel)
        self.layout.addWidget(self.export_button)

        # 🔧 Beállítások gomb
        self.settings_button = QPushButton("⚙️ Beállítások")
        self.settings_button.clicked.connect(self.open_settings)
        self.layout.addWidget(self.settings_button)

        self.stats_button = QPushButton("📊 Heti statisztika")
        self.stats_button.clicked.connect(self.show_stats)
        self.layout.addWidget(self.stats_button)


        self.analysis_button = QPushButton("🧠 Elemzés")
        self.analysis_button.clicked.connect(self.show_analysis)
        self.layout.addWidget(self.analysis_button)


        self.dashboard_button = QPushButton("📈 AI Dashboard")
        self.dashboard_button.clicked.connect(self.show_dashboard)
        self.layout.addWidget(self.dashboard_button)

    def show_dashboard(self):
        tasks = self.task_manager.get_all_tasks()
        dialog = DashboardWindow(tasks)
        dialog.exec()



    def show_analysis(self):
        tasks = self.task_manager.get_all_tasks()
        dialog = AnalysisWindow(tasks)
        dialog.exec()



    def show_stats(self):
        tasks = self.task_manager.get_all_tasks()
        dialog = StatsWindow(tasks)
        dialog.exec()


    def open_settings(self):
        dialog = SettingsWindow()
        dialog.exec()

    def export_to_excel(self):
        filepath = export_tasks_to_excel(self.task_manager.get_all_tasks())
        QMessageBox.information(self, "Sikeres export", f"Exportálva:\n{filepath}")

    def show_task_list(self):
        tasks = self.task_manager.get_all_tasks()
        dialog = TaskListWindow(tasks)
        dialog.exec()


    def start_task(self):
        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "Hiányzó cím", "Kérlek adj meg egy feladatcímet!")
            return

        # 🔮 Előrejelzés
        prediction = predict_duration(title, description, self.task_manager.get_all_tasks())
        if prediction is not None:
            QMessageBox.information(self, "AI becslés", f"A rendszer szerint ez a feladat kb. {prediction} percet vehet igénybe.")
        else:
            print("⚠️ Nincs elég adat az előrejelzéshez.")


        task = self.task_manager.create_task(title, description)
        self.task_manager.start_current_task()
        self.status_label.setText(f"Futó feladat: {task.title} | Becslés: {prediction} perc")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
    

    def stop_task(self):
        self.task_manager.stop_current_task()
        task = self.task_manager.get_active_task()
        duration = task.get_duration()
        self.status_label.setText(f"Feladat lezárva: {task.title} | Időtartam: {duration}")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        dialog = CloseTaskDialog()
        result = dialog.exec()

        if result == QDialog.Accepted:
            notes = dialog.get_notes()
            if notes:
                task.log_event(f"Záró megjegyzés: {notes}")

            self.status_label.setText(f"Feladat lezárva: {task.title} | Időtartam: {duration}")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

        for t in self.task_manager.get_all_tasks():
            for log in t.logs:
                print(log)

        self.task_manager.check_auto_archive(self)
