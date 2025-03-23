from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict

class TaskTimelineWindow(QDialog):
    def __init__(self, task, on_new_task_callback=None):
        super().__init__()
        self.setWindowTitle(f"Idővonal: {task.title}")
        self.resize(1000, 600)
        self.task = task
        self.on_new_task_callback = on_new_task_callback

        self.selected_start = None
        self.selected_end = None
        self.selection_patch = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.create_button = QPushButton("Új feladat a kijelölésből")
        self.create_button.clicked.connect(self.create_task_from_selection)
        self.layout.addWidget(self.create_button)

        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.plot_timeline()

    def plot_timeline(self):
        self.ax.clear()

        if not self.task.logs:
            self.ax.text(0.5, 0.5, "Nincs napló ehhez a feladathoz.", ha='center', va='center', fontsize=12)
            self.canvas.draw()
            return

        start_time = self.task.start_time
        grouped = defaultdict(list)

        # Csoportosítás ablakcímek szerint
        for timestamp, message in self.task.logs:
            if message.startswith("Aktív ablak:"):
                title = message.replace("Aktív ablak: ", "").strip()
                grouped[title].append(timestamp)

        if not grouped:
            self.ax.text(0.5, 0.5, "Nem található aktív ablak információ.", ha='center', va='center', fontsize=12)
            self.canvas.draw()
            return

        y_labels = list(grouped.keys())
        y_ticks = list(range(len(y_labels)))

        for i, (title, times) in enumerate(grouped.items()):
            for ts in times:
                rel_minutes = (ts - start_time).total_seconds() / 60
                self.ax.barh(i, 0.5, left=rel_minutes, height=0.4, color='skyblue')
                self.ax.text(rel_minutes, i + 0.1, ts.strftime("%H:%M"), fontsize=7, rotation=45)

        self.ax.set_yticks(y_ticks)
        self.ax.set_yticklabels(y_labels)
        self.ax.set_xlabel("Percek a kezdéstől")
        self.ax.set_title("Aktív ablakok idővonala")

        self.figure.tight_layout()
        self.canvas.draw()

    def on_click(self, event):
        if not event.xdata:
            return

        # Jobb egér: törlés
        if event.button == 3:
            self.selected_start = None
            self.selected_end = None
            self.selection_patch = None
            self.plot_timeline()
            return

        # Bal egér: kijelölés
        if event.button == 1:
            if self.selected_start is None:
                self.selected_start = event.xdata
                self.ax.axvline(self.selected_start, color='orange', linestyle='--')
            else:
                self.selected_end = event.xdata
                if self.selected_start > self.selected_end:
                    self.selected_start, self.selected_end = self.selected_end, self.selected_start

                self.selection_patch = self.ax.axvspan(
                    self.selected_start, self.selected_end, color='orange', alpha=0.3
                )

            self.canvas.draw()

    def create_task_from_selection(self):
        if self.selected_start is None or self.selected_end is None:
            QMessageBox.warning(self, "Nincs kijelölés", "Kérlek jelöld ki az időintervallumot a grafikonon.")
            return

        start_time = self.task.start_time + timedelta(minutes=self.selected_start)
        end_time = self.task.start_time + timedelta(minutes=self.selected_end)

        selected_logs = [
            (ts, msg)
            for ts, msg in self.task.logs
            if start_time <= ts <= end_time
        ]

        if not selected_logs:
            QMessageBox.information(self, "Nincs napló az intervallumban", "A kijelölt időszakban nem történt esemény.")
            return

        title = f"Részfeladat – {self.task.title}"
        description = f"Létrehozva idővonal alapján ({start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')})"

        if self.on_new_task_callback:
            self.on_new_task_callback(title, description, selected_logs)
            QMessageBox.information(self, "Új feladat", "Az új feladat elmentve.")
            self.close()
