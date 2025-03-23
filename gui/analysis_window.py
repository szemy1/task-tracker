# gui/analysis_window.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit
from collections import defaultdict
import datetime
from core.tag_suggester import suggest_tag
from gui.style import modern_style
from PySide6.QtWidgets import QHBoxLayout, QPushButton
from PySide6.QtCore import Qt

class AnalysisWindow(QDialog):
    def __init__(self, tasks):
        super().__init__()
        self.setWindowTitle("📊 AI-alapú feladatelemzés")
        self.resize(600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
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

        label = QLabel("🧠 Elemzés és következtetések:")
        layout.addWidget(label)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.analyze_tasks(tasks)

    def analyze_tasks(self, tasks):
        tag_duration = defaultdict(float)
        day_totals = defaultdict(float)
        hour_distribution = defaultdict(int)

        for task in tasks:
            logs = task.logs
            for i in range(1, len(logs)):
                t1, msg1 = logs[i - 1]
                t2, _ = logs[i]
                delta = (t2 - t1).total_seconds() / 60  # perc

                tag = "egyéb"
                if "Típus:" in msg1:
                    tag = msg1.split("Típus:")[-1].strip().lower()
                else:
                    tag = suggest_tag(msg1)

                tag_duration[tag] += delta
                day_name = t1.strftime('%A')
                day_totals[day_name] += delta
                hour_distribution[t1.hour] += 1

        output = []

        if tag_duration:
            top_tag = max(tag_duration, key=tag_duration.get)
            output.append(f"🟢 Legtöbb idő a(z) **{top_tag}** címkére ment el: {tag_duration[top_tag]:.1f} perc")

        if day_totals:
            most_productive_day = max(day_totals, key=day_totals.get)
            output.append(f"📅 Legaktívabb napod: **{most_productive_day}** ({day_totals[most_productive_day]:.1f} perc)")

        if hour_distribution:
            peak_hour = max(hour_distribution, key=hour_distribution.get)
            output.append(f"⏰ Leggyakoribb aktív órád: **{peak_hour}:00 - {peak_hour+1}:00**")

        if tag_duration.get("szünet", 0) > sum(tag_duration.values()) * 0.4:
            output.append("⚠️ Figyelem: a szünetek aránya kiemelkedően magas! 🤔")

        if not output:
            output.append("Nincs elég adat az elemzéshez.")

        self.output.setText("\n\n".join(output))
