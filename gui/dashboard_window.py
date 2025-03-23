
# gui/dashboard_window.py

from PySide6.QtWidgets import QDialog, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from collections import defaultdict
import datetime
from core.tag_suggester import suggest_tag
from gui.style import modern_style
from PySide6.QtWidgets import QHBoxLayout, QPushButton
from PySide6.QtCore import Qt

class DashboardWindow(QDialog):
    def __init__(self, tasks):
        super().__init__()
        self.setWindowTitle("📊 AI Dashboard")
        self.resize(900, 700)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

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
        self.setStyleSheet(modern_style)


        self.figure = Figure(figsize=(10, 7))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.plot_dashboard(tasks)

    def plot_dashboard(self, tasks):
        tag_duration = defaultdict(float)
        daily_totals = defaultdict(float)
        hour_distribution = defaultdict(int)

        for task in tasks:
            logs = task.logs
            for i in range(1, len(logs)):
                t1, msg1 = logs[i - 1]
                t2, _ = logs[i]
                delta = (t2 - t1).total_seconds() / 60  # perc

                if "Típus:" in msg1:
                    tag = msg1.split("Típus:")[-1].strip().lower()
                else:
                    tag = suggest_tag(msg1)

                tag_duration[tag] += delta
                daily_totals[t1.strftime('%A')] += delta
                hour_distribution[t1.hour] += 1

        self.figure.clear()
        ax1 = self.figure.add_subplot(221)  # Kördiagram - címkék
        ax2 = self.figure.add_subplot(222)  # Oszlopdiagram - napi aktivitás
        ax3 = self.figure.add_subplot(212)  # Hisztogram - óránkénti aktivitás

        # Címke kördiagram
        tags = list(tag_duration.keys())
        durations = list(tag_duration.values())
        ax1.pie(durations, labels=tags, autopct='%1.1f%%')
        ax1.set_title("Időmegoszlás címkék szerint")

        # Napi aktivitás
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        values = [daily_totals.get(day, 0) for day in days_order]
        ax2.bar(days_order, values)
        ax2.set_title("Napi aktivitás")
        ax2.tick_params(axis='x', rotation=45)

        # Óránkénti aktivitás
        hours = list(range(24))
        counts = [hour_distribution.get(h, 0) for h in hours]
        ax3.bar(hours, counts)
        ax3.set_title("Óránkénti aktivitás")
        ax3.set_xlabel("Óra")
        ax3.set_ylabel("Események száma")

        self.figure.tight_layout()
        self.canvas.draw()
