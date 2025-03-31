import os
import shutil
from datetime import datetime
import json

class Storage:
    def __init__(self, filepath=os.path.join(os.path.dirname(__file__), "tasks.json")):
        self.file_path = filepath
        self.archive_folder = os.path.join(os.path.dirname(__file__), "archive")


    def load_tasks(self):
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            return []
        with open(self.file_path, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def save_tasks(self, tasks):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)

    def check_and_archive(self, tasks):
        if len(tasks) >= 50 or os.path.getsize(self.file_path) > 1024 * 1024:
            os.makedirs(self.archive_folder, exist_ok=True)
            archive_file = os.path.join(
                self.archive_folder, f"tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            shutil.move(self.file_path, archive_file)
            self.save_tasks([])
