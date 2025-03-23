# core/task_manager.py

import time
from datetime import datetime
from core import storage
from core.app_logger import AppLogger


class Task:
    def __init__(self, title: str, description: str = ""):
        self.title = title
        self.description = description
        self.start_time = None
        self.end_time = None
        self.logs = []
        self.is_active = False

    def start(self):
        self.start_time = datetime.now()
        self.is_active = True
        self.log_event("Feladat indítva")

    def pause(self):
        self.is_active = False
        self.log_event("Feladat szüneteltetve")

    def resume(self):
        self.is_active = True
        self.log_event("Feladat folytatva")

    def stop(self):
        self.end_time = datetime.now()
        self.is_active = False
        self.log_event("Feladat lezárva")

    def log_event(self, message: str):
        timestamp = datetime.now()
        self.logs.append((timestamp, message))

    def get_duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        elif self.start_time:
            return datetime.now() - self.start_time
        else:
            return None

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "logs": [(ts.isoformat(), msg) for ts, msg in self.logs],
        }

    def __str__(self):
        duration = self.get_duration()
        return f"{self.title} - {duration}"


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.current_task = None
        self.logger = None

        self._load_tasks()

    def _load_tasks(self):
        raw_tasks = storage.load_tasks()
        self.tasks = []

        for data in raw_tasks:
            task = Task(
                title=data["title"],
                description=data["description"]
            )
            if data.get("start_time"):
                task.start_time = datetime.fromisoformat(data["start_time"])
            if data.get("end_time"):
                task.end_time = datetime.fromisoformat(data["end_time"])
            for ts, msg in data["logs"]:
                task.logs.append((datetime.fromisoformat(ts), msg))

            self.tasks.append(task)

    def save(self):
        storage.save_tasks(self.tasks)

    def check_auto_archive(self, parent=None):
        return storage.check_archive_needed(self.tasks, ask_user=True, parent=parent)

    def create_task(self, title: str, description: str = ""):
        task = Task(title, description)
        self.tasks.append(task)
        self.current_task = task
        return task

    def start_current_task(self, notifier):
        if self.current_task:
            self.current_task.start()
            self.logger = AppLogger(self, notifier)  # ✅ ÁTADJUK A TASKMANAGER-T
            self.logger.start()

    def stop_current_task(self):
        if self.current_task:
            self.current_task.stop()
        if self.logger:
            self.logger.stop()
            self.logger = None
        self.save()

    def get_active_task(self):
        return self.current_task

    def get_all_tasks(self):
        return self.tasks
