# backend/api/tasks.py
from fastapi import APIRouter, HTTPException, Body
from backend.api.schemas import TaskSchema, Task
from typing import List, Optional
from backend.core.task_manager import get_shared_task_manager
from backend.api.schemas import TaskTemplateSchema
from backend.core.task_storage import task_storage


router = APIRouter()
task_manager = get_shared_task_manager()

# --- CÍM ALAPÚ ROUTE-OK ELŐL ---
@router.get("/title/{title}")
def get_task_by_title(title: str):
    task = task_manager.get_task_by_title(title)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found by title")
    return task


@router.put("/title/{title}")
def update_task_by_title(title: str, updated_data: dict):
    updated_task = task_manager.update_task_by_title(title, updated_data)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found for update by title")
    return updated_task

# --- TÖBBI FUNKCIÓ ---

@router.get("/", response_model=List[Task])
def get_tasks(status: Optional[str] = None, search: Optional[str] = None):
    tasks = task_manager.get_all_tasks()

    if status:
        tasks = [task for task in tasks if task.get("status", "").lower() == status.lower()]
    if search:
        tasks = [task for task in tasks if search.lower() in task["name"].lower() or search.lower() in task["description"].lower()]

    return tasks


# backend/api/tasks.py vagy ahol a routered van

@router.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    task = task_storage.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task



@router.post("/", response_model=Task)
def create_task(task: TaskSchema):
    return task_manager.add_task(
        title=task.name,
        description=task.description,
        status=task.status,
        window_title=task.window_title
    )


@router.put("/{task_id}")
def update_task(task_id: int, updated_data: dict = Body(...)):
    updated_task = task_manager.update_task(task_id, updated_data)
    if updated_task:
        return updated_task
    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}")
def delete_task(task_id: int):
    if task_manager.delete_task(task_id):
        return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/{task_id}/start")
def start_task(task_id: int):
    started_task = task_manager.start_task(task_id)
    if started_task:
        return started_task
    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/{task_id}/stop")
def stop_task(task_id: int):
    stopped_task = task_manager.stop_task(task_id)
    if stopped_task:
        return stopped_task
    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/suggest", response_model=Task)
def suggest_task(template_data: TaskTemplateSchema = Body(...)):
    templates = {
        "default": {
            "description": "Új feladat a rendszerben",
            "status": "open"
        },
        "docs": {
            "description": "Dokumentáció frissítése",
            "status": "planned"
        },
        "bugfix": {
            "description": "Hibajavítás szükséges",
            "status": "open"
        }
    }

    selected = templates.get(template_data.template, templates["default"])
    description = f"{selected['description']}\n\nJegyzet: {template_data.notes}"

    return task_manager.add_task(
        title=template_data.title,
        description=description,
        status=selected["status"],
        window_title=template_data.window_title
    )
