from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TaskSchema(BaseModel):
    name: str
    description: Optional[str] = ""
    status: Optional[str] = "open"
    window_title: Optional[str] = None

class Task(BaseModel):
    id: int
    title: str  # 👈 ez hiányzott
    name: str
    description: str
    status: str = "open"
    start_time: datetime
    end_time: Optional[datetime]
    logs: List[dict]
    duration: Optional[str] = None  # 👈 opcionális mező, ha számított értékként visszajön



class TaskTemplateSchema(BaseModel):
    title: str
    template: Optional[str] = "default"
    notes: Optional[str] = ""
    window_title: Optional[str] = None
