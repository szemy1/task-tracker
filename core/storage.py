# core/storage.py

import os
import json
from datetime import datetime
from PySide6.QtWidgets import QMessageBox

DATA_FILE = "data/tasks.json"
ARCHIVE_FOLDER = "archive"
ARCHIVE_LIMIT_TASKS = 50      # Feladat limit archiváláshoz
ARCHIVE_LIMIT_MB = 1          # Max fájlméret MB-ban

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
        return raw

def save_tasks(tasks):
    os.makedirs("data", exist_ok=True)

    # Objektumok → dict (sorosítás)
    task_data = []
    for t in tasks:
        task_data.append({
            "title": t.title,
            "description": t.description,
            "start_time": t.start_time.isoformat() if t.start_time else None,
            "end_time": t.end_time.isoformat() if t.end_time else None,
            "logs": [(ts.isoformat(), msg) for ts, msg in t.logs]
        })

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(task_data, f, indent=4, ensure_ascii=False)

def check_archive_needed(tasks, ask_user=False, parent=None):
    # Fájlméret MB
    file_size_mb = 0
    if os.path.exists(DATA_FILE):
        file_size_mb = os.path.getsize(DATA_FILE) / (1024 * 1024)

    if len(tasks) >= ARCHIVE_LIMIT_TASKS or file_size_mb >= ARCHIVE_LIMIT_MB:
        if ask_user:
            result = QMessageBox.question(
                parent,
                "Archiválás szükséges",
                "A feladatok száma vagy mérete elérte a határt.\n"
                "Szeretnéd most archiválni?",
                QMessageBox.Yes | QMessageBox.No
            )
            if result == QMessageBox.Yes:
                archive_and_clear(tasks)
                return True
        else:
            archive_and_clear(tasks)
            return True
    return False

def archive_and_clear(tasks):
    os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    archive_path = os.path.join(ARCHIVE_FOLDER, f"tasks_{timestamp}.json")

    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump([task.to_dict() for task in tasks], f, indent=4, ensure_ascii=False)


    # Kiürítjük az aktuális adatbázist
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4, ensure_ascii=False)

    print(f"[Archiválva]: {archive_path}")
