from backend.data.storage import Storage
from datetime import datetime
import logging

class TaskManager:
    def __init__(self):
        self.storage = Storage()

    def get_all_tasks(self):
        tasks = self.storage.load_tasks()
        for task in tasks:
            if "title" not in task:
                task["title"] = task.get("name", "Untitled")  # ⬅️ default ha nincs title
            if task.get("start_time") and task.get("end_time"):
                start = datetime.fromisoformat(task["start_time"])
                end = datetime.fromisoformat(task["end_time"])
                task["duration"] = str(end - start)
        return tasks


    def generate_unique_title(self, base: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base}_{timestamp}"
    
    def _generate_title(self, window_title=None):
        title = window_title or "Task"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{title}_{timestamp}"

    def add_task(self, title=None, description="", status="open", window_title=None):  # ⬅️ window_title paraméter itt is kell
        tasks = self.storage.load_tasks()
        new_id = max([task.get("id", 0) for task in tasks], default=0) + 1

        generated_title = self._generate_title(window_title)
        task_data = {
            "id": new_id,
            "title": generated_title,  # 👈 külön mező, belső azonosítóhoz
            "name": title or generated_title,  # fallback ha a name nincs megadva
            "description": description,
            "status": status,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "logs": [{"timestamp": datetime.now().isoformat(), "message": "Feladat elindítva"}]
        }
        tasks.append(task_data)
        self.storage.save_tasks(tasks)
        logging.info(f"Feladat hozzáadva: {new_id}")
        self.storage.check_and_archive(tasks)
        return task_data


    def update_task(self, task_id, updated_data):
        tasks = self.storage.load_tasks()
        for task in tasks:
            if int(task["id"]) == int(task_id):
                task.update(updated_data)
                task["logs"].append({"timestamp": datetime.now().isoformat(), "message": "Feladat frissítve"})
                self.storage.save_tasks(tasks)
                self.storage.check_and_archive(tasks)
                return task
        return None

    def update_task_by_title(self, title, updated_data):
        tasks = self.storage.load_tasks()
        for task in tasks:
            if task.get("title") == title:
                task.update(updated_data)
                task["logs"].append({"timestamp": datetime.now().isoformat(), "message": "Feladat frissítve (cím alapján)"})
                self.storage.save_tasks(tasks)
                self.storage.check_and_archive(tasks)
                return task
        return None

    def get_task_by_title(self, title):
        tasks = self.storage.load_tasks()
        return next((task for task in tasks if task.get("title") == title), None)

    def close_task(self, task_id):
        return self.update_task(task_id, {"end_time": datetime.now().isoformat()})

    def delete_task(self, task_id):
        tasks = self.storage.load_tasks()
        new_tasks = [task for task in tasks if int(task["id"]) != int(task_id)]
        if len(tasks) != len(new_tasks):
            self.storage.save_tasks(new_tasks)
            logging.info(f"Feladat törölve: {task_id}")
            self.storage.check_and_archive(new_tasks)
            return True
        return False

    def start_task(self, task_id):
        tasks = self.storage.load_tasks()
        for task in tasks:
            if int(task["id"]) == int(task_id):
                task["status"] = "in_progress"
                task["logs"].append({
                    "timestamp": datetime.now().isoformat(),
                    "message": "Feladat elindítva"
                })
                self.storage.save_tasks(tasks)
                self.storage.check_and_archive(tasks)
                return task
        return None

    def stop_task(self, task_id):
        tasks = self.storage.load_tasks()
        for task in tasks:
            if int(task["id"]) == int(task_id):
                task["status"] = "completed"
                task["end_time"] = datetime.now().isoformat()
                task["logs"].append({
                    "timestamp": datetime.now().isoformat(),
                    "message": "Feladat leállítva"
                })
                self.storage.save_tasks(tasks)
                self.storage.check_and_archive(tasks)
                return task
        return None

# Globális példány létrehozása
_task_manager_instance = None

def get_shared_task_manager():
    global _task_manager_instance
    if _task_manager_instance is None:
        _task_manager_instance = TaskManager()
    return _task_manager_instance
