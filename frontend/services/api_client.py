import httpx
import requests


class APIClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    def get_tasks(self):
        url = f"{self.base_url}/tasks/"
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()

    def create_task(self, title: str, description: str):
        payload = {
            "name": title,
            "description": description,
            "status": "in_progress",
            "window_title": ""
        }
        response = requests.post(f"{self.base_url}/tasks", json=payload)
        response.raise_for_status()
        task = response.json()
        if "id" not in task:
            print("[HIBA] Visszakapott task nem tartalmaz id-t:", task)
        return task


    
    def update_task(self, task_id: int, title=None, description=None, status=None):
        payload = {}
        if title:
            payload["name"] = title
        if description:
            payload["description"] = description
        if status:
            payload["status"] = status

        response = requests.put(f"{self.base_url}/tasks/{task_id}", json=payload)
        response.raise_for_status()
        return response.json()



    def delete_task(self, task_id):
        url = f"{self.base_url}/tasks/{task_id}"
        response = httpx.delete(url)
        response.raise_for_status()
        return response.json()

    def start_task(self, task_id: int, title=None, description=None):
        payload = {}
        if title:
            payload["title"] = title
        if description:
            payload["description"] = description

        response = requests.post(f"{self.base_url}/tasks/{task_id}/start", json=payload)
        response.raise_for_status()
        return response.json()


    def stop_task(self, task_id: int):
        response = requests.post(f"{self.base_url}/tasks/{task_id}/stop")
        response.raise_for_status()
        return response.json()
