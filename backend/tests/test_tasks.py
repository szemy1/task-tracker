# backend/tests/test_tasks.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from datetime import timedelta

client = TestClient(app)

@pytest.fixture
def new_task():
    return {
        "name": "Teszt Feladat",
        "description": "Teszt leírás",
        "status": "open"
    }

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "TimeTracker API működik."}

def test_create_task(new_task):
    response = client.post("/tasks/", json=new_task)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == new_task["name"]

def test_get_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_task(new_task):
    response_create = client.post("/tasks/", json=new_task)
    task_id = response_create.json()["id"]

    updated_data = {
        "name": "Frissített Feladat",
        "description": "Frissített leírás",
        "status": "closed"
    }

    response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Frissített Feladat"
    assert data["status"] == "closed"

def test_delete_task(new_task):
    response_create = client.post("/tasks/", json=new_task)
    task_id = response_create.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    response_check = client.get("/tasks/")
    assert all(task["id"] != task_id for task in response_check.json())

def test_start_and_stop_task():
    task = {"name": "Indítás Teszt", "description": "Egy induló task", "status": "open"}
    create_resp = client.post("/tasks/", json=task)
    task_id = create_resp.json()["id"]

    start_resp = client.post(f"/tasks/{task_id}/start")
    assert start_resp.status_code == 200
    assert start_resp.json()["status"] == "in_progress"

    stop_resp = client.post(f"/tasks/{task_id}/stop")
    assert stop_resp.status_code == 200
    assert stop_resp.json()["status"] == "completed"
    assert stop_resp.json()["end_time"] is not None

def test_suggest_task():
    suggest_data = {
        "title": "Ajánlott feladat",
        "template": "docs",
        "notes": "Swagger dokumentáció hiányos"
    }
    response = client.post("/tasks/suggest", json=suggest_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "Swagger" in data["description"]
    assert data["status"] == "planned"



def test_task_duration_field():
    task = {"name": "Időtartam Teszt", "description": "Mérjük az időtartamot", "status": "open"}
    create = client.post("/tasks/", json=task)
    task_id = create.json()["id"]

    client.post(f"/tasks/{task_id}/start")
    client.post(f"/tasks/{task_id}/stop")

    all_tasks = client.get("/tasks/").json()
    matching = [t for t in all_tasks if t["id"] == task_id]

    assert len(matching) == 1, f"Nem található a task ID: {task_id}, tasks: {all_tasks}"
    assert "duration" in matching[0]

    # 🔄 Convert str -> timedelta
    time_parts = matching[0]["duration"].split(":")
    seconds = float(time_parts[-1]) + int(time_parts[-2]) * 60 + int(time_parts[-3]) * 3600

    assert seconds > 0


# backend/tests/test_tasks.py

def test_get_task_by_title(new_task):
    created = client.post("/tasks/", json=new_task).json()
    title = created["title"]
    response = client.get(f"/tasks/title/{title}")
    assert response.status_code == 200
    assert response.json()["title"] == title


def test_update_task_by_title(new_task):
    created = client.post("/tasks/", json=new_task).json()
    title = created["title"]
    updated_data = {
        "name": "Cím alapján frissítve",
        "description": "Frissítés title alapján",
        "status": "closed"
    }
    response = client.put(f"/tasks/title/{title}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]


def test_delete_task_invalid_id():
    response = client.delete("/tasks/99999")  # nem létező ID
    assert response.status_code in (404, 200)  # attól függ, hogy kezeled-e külön


def test_start_task(new_task):
    created = client.post("/tasks/", json=new_task).json()
    task_id = created["id"]
    response = client.post(f"/tasks/{task_id}/start")
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


def test_stop_task(new_task):
    created = client.post("/tasks/", json=new_task).json()
    task_id = created["id"]
    client.post(f"/tasks/{task_id}/start")
    response = client.post(f"/tasks/{task_id}/stop")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
