from fastapi import APIRouter
from fastapi.responses import FileResponse
from backend.core.task_manager import TaskManager
import openpyxl
import os

router = APIRouter()
task_manager = TaskManager()

EXPORT_FILE_PATH = "exported_tasks.xlsx"

@router.get("/tasks/excel")
def export_tasks_excel():
    tasks = task_manager.get_all_tasks()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tasks"

    # fejléc
    ws.append(["ID", "Name", "Description", "Status"])

    # adatok
    for task in tasks:
        ws.append([
            task["id"],
            task["name"],
            task.get("description", ""),
            task["status"]
        ])

    wb.save(EXPORT_FILE_PATH)

    return FileResponse(EXPORT_FILE_PATH, filename="tasks.xlsx")
