# backend/main.py

from fastapi import FastAPI
from backend.api import tasks

app = FastAPI()

# Csatoljuk a /tasks útvonal alá az összes feladat API-t
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# Gyökérútvonal csak teszteléshez
@app.get("/")
def root():
    return {"message": "TimeTracker API működik."}
