# backend/core/task_timer_manager.py

from datetime import datetime, timedelta

class TaskTimerManager:
    def __init__(self):
        self.active_task_id = None
        self.start_time = None

    def start_task(self, task_id: str):
        if self.active_task_id == task_id:
            return  # már fut
        self.active_task_id = task_id
        self.start_time = datetime.now()

    def stop_task(self):
        if not self.active_task_id or not self.start_time:
            return None
        elapsed = datetime.now() - self.start_time
        stopped_task = {
            "task_id": self.active_task_id,
            "start_time": self.start_time,
            "elapsed_seconds": elapsed.total_seconds()
        }
        self.active_task_id = None
        self.start_time = None
        return stopped_task

    def get_active_task(self):
        if not self.active_task_id or not self.start_time:
            return None
        elapsed = datetime.now() - self.start_time
        return {
            "task_id": self.active_task_id,
            "start_time": self.start_time,
            "elapsed": str(elapsed).split(".")[0]  # HH:MM:SS
        }
