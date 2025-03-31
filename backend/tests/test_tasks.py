import pytest
from fastapi.testclient import TestClient
from backend.main import app

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
    tasks = response.json()
    assert isinstance(tasks, list)

def test_update_task(new_task):
    # Létrehozunk egy új feladatot
    response_create = client.post("/tasks/", json=new_task)
    task_id = response_create.json()["id"]

    updated_data = {
        "name": "Frissített Feladat",
        "description": "Frissített leírás",
        "status": "closed"
    }

    response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["name"] == "Frissített Feladat"
    assert updated_task["status"] == "closed"

def test_delete_task(new_task):
    # Létrehozunk egy új feladatot, majd töröljük
    response_create = client.post("/tasks/", json=new_task)
    task_id = response_create.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}

    # Ellenőrizzük, hogy valóban törölve lett-e
    response_after_delete = client.get("/tasks/")
    assert all(task["id"] != task_id for task in response_after_delete.json())

