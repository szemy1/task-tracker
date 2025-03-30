from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QSettings, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
import os
import json
from gui.style import get_theme_style
from datetime import datetime
from collections import defaultdict
from datetime import timedelta
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QObject, Slot
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile



def format_time(dt: datetime):
    return dt.replace(microsecond=0).isoformat(timespec='seconds')



class TaskTimelineWindow(QDialog):
    def __init__(self, task, on_new_task_callback=None):
        super().__init__()
        self.setWindowTitle(f"Idővonal: {task.title}")
        self.resize(1000, 600)
        self.task = task
        self.on_new_task_callback = on_new_task_callback

        theme = QSettings().value("theme", "dark")
        self.setStyleSheet(get_theme_style(theme))

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Top bar with close button
        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignRight)
        close_button = QPushButton("✖")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("border: none; font-size: 16px;")
        close_button.clicked.connect(self.close)
        top_bar.addWidget(close_button)
        layout.addLayout(top_bar)

        # Create temporary task.json to inject into webview
        self.inject_task_data()

        # WebView for the modern Gantt chart
        self.web_view = QWebEngineView()
        index_path = os.path.abspath("webui/index.html")
        print("📄 Betöltött index.html:", index_path)
        self.web_view.load(QUrl.fromLocalFile(index_path))

        # WebView for the modern timeline
        self.web_view = QWebEngineView()


        # ✅ Betöltjük a timeline nézetet
        index_path = os.path.abspath("webui/index.html")
        self.web_view.load(QUrl.fromLocalFile(index_path))

        # 🛠️ DevTools ablak csatlakoztatása
        devtools = QWebEngineView(self)
        devtools.setWindowTitle("DevTools - vis-timeline")
        devtools.resize(800, 600)
        devtools.show()

        devtools_page = QWebEnginePage(QWebEngineProfile.defaultProfile(), devtools)
        devtools.setPage(devtools_page)

        # 💡 Csatoljuk a devtools oldalt a fő nézethez
        self.web_view.page().setDevToolsPage(devtools_page)


        # ➕ WebChannel összekötés
        self.channel = QWebChannel()
        self.js_bridge = JSBridge(self.on_new_task_callback)
        self.channel.registerObject("api", self.js_bridge)
        self.web_view.page().setWebChannel(self.channel)




    def inject_task_data(self):
        log_entries = getattr(self.task, "logs", [])

        active_tasks = {}
        parsed_tasks = []

        for timestamp_str, message in log_entries:
            timestamp = timestamp_str if isinstance(timestamp_str, datetime) else datetime.fromisoformat(timestamp_str)

            if message.startswith("Start: "):
                title = message.replace("Start: ", "").strip()
                active_tasks[title] = timestamp
            elif message.startswith("End: "):
                title = message.replace("End: ", "").strip()
                if title in active_tasks:
                    start_time = active_tasks.pop(title)
                    if start_time == timestamp:
                        timestamp += timedelta(minutes=1)
                    parsed_tasks.append({
                        "id": title,
                        "name": title,
                        "start": format_time(start_time),
                        "end": format_time(timestamp),
                        "progress": 100
                    })

        # Fallback: ha nincs log, legalább a főtaskot is kirakjuk
        if not parsed_tasks:
            if self.task.start_time == self.task.end_time:
                self.task.end_time += timedelta(minutes=1)

            parsed_tasks.append({
                "id": self.task.title,
                "name": self.task.title,
                "start": format_time(self.task.start_time),
                "end": format_time(self.task.end_time),
                "progress": 100
            })

        # Írjuk ki a tasks.json fájlt
        tasks_path = os.path.abspath("webui/tasks.json")
        with open(tasks_path, "w", encoding="utf-8") as f:
            json.dump(parsed_tasks, f, ensure_ascii=False, indent=2)
        print(f"✅ tasks.json generálva: {tasks_path}")


class JSBridge(QObject):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    @Slot(dict)
    def create_subtask(self, task_data):
        if self.callback:
            self.callback({
                "title": task_data["name"],
                "start_time": task_data["start"],
                "end_time": task_data["end"]
            })
