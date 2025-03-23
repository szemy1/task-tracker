# gui/stats_window.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from collections import defaultdict
import matplotlib.dates as mdates
import datetime
from PySide6.QtWidgets import QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
from core.tag_suggester import suggest_tag
from gui.style import modern_style


class StatsWindow(QDialog):
    def __init__(self, tasks):
        super().__init__()
        self.setWindowTitle("Heti statisztika")
        self.resize(800, 500)
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
        self.setLayout(layout)
        self.setStyleSheet(modern_style)


        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.plot_data(tasks)

    def plot_data(self, tasks):
        data = defaultdict(lambda: defaultdict(float))  # nap -> címke -> idő percben

        for task in tasks:
            logs = task.logs
            for i in range(1, len(logs)):
                t1, msg1 = logs[i - 1]
                t2, msg2 = logs[i]
                delta = (t2 - t1).total_seconds() / 60  # perc

                if "Típus:" in msg1:
                    tag = msg1.split("Típus:")[-1].strip().lower()
                else:
                    tag = suggest_tag(msg1)

                weekday = t1.strftime('%a')  # Pl.: 'Mon', 'Tue'
                data[weekday][tag] += delta

        ax = self.figure.add_subplot(111)
        ax.clear()

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        tags = set(tag for day in data.values() for tag in day)

        bottom = [0] * len(days)

        for tag in tags:
            values = [data[day].get(tag, 0) for day in days]
            ax.bar(days, values, bottom=bottom, label=tag)
            bottom = [b + v for b, v in zip(bottom, values)]

        ax.set_title("Heti időfelhasználás címke szerint")
        ax.set_ylabel("Idő (perc)")
        ax.legend()
        self.figure.tight_layout()
        self.canvas.draw()
