import json
import os

TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

class Storage:
    def load_tasks(self):
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_tasks(self, tasks):
        with open(TASKS_FILE, 'w', encoding='utf-8') as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)
