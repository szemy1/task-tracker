from fastapi import APIRouter, HTTPException
from backend.core.task_manager import TaskManager
from pydantic import BaseModel
from typing import List
from typing import Optional

router = APIRouter()

task_manager = TaskManager()

# Ez a meglévő feladatokat reprezentálja (ID-vel együtt)
class Task(BaseModel):
    id: int
    name: str
    description: str = ""
    status: str = "open"

# Ez a modell az új feladatok létrehozásához kell (ID nélkül)
class TaskCreate(BaseModel):
    name: str
    description: str = ""
    status: str = "open"

@router.get("/", response_model=List[Task])
def get_tasks():
    tasks = task_manager.get_all_tasks()
    return tasks

@router.post("/", response_model=Task)
def create_task(task: TaskCreate):  # <-- itt TaskCreate használandó!
    created_task = task_manager.add_task(task.model_dump())
    return created_task


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate):
    updated_task = task_manager.update_task(task_id, task.model_dump())
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}")
def delete_task(task_id: int):
    deleted = task_manager.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.get("/", response_model=List[Task])
def get_tasks(status: Optional[str] = None, search: Optional[str] = None):
    tasks = task_manager.get_all_tasks()

    if status:
        tasks = [task for task in tasks if task["status"].lower() == status.lower()]

    if search:
        tasks = [
            task for task in tasks
            if search.lower() in task["name"].lower() or search.lower() in task["description"].lower()
        ]

    return tasks