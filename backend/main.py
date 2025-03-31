from fastapi import FastAPI
from backend.api.tasks import router as tasks_router
from backend.api.export import router as export_router
from backend.utils.logger import setup_logger
from backend.utils.logging_middleware import log_requests
import os

DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

app = FastAPI(title="TimeTracker API", debug=DEBUG_MODE)

setup_logger(debug_mode=DEBUG_MODE)

# Middleware beállítás (automatikus logolás minden kérésre)
if DEBUG_MODE:
    app.middleware("http")(log_requests)

app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
app.include_router(export_router, prefix="/export", tags=["Export"])

@app.get("/")
def root():
    return {"message": "TimeTracker API működik."}
