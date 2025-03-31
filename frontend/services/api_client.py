import httpx

class APIClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    def get_tasks(self):
        url = f"{self.base_url}/tasks/"
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()

    def create_task(self, task_data):
        url = f"{self.base_url}/tasks/"
        response = httpx.post(url, json=task_data)
        response.raise_for_status()
        return response.json()
    
    def create_task(self, task_data):
        url = f"{self.base_url}/tasks/"
        response = httpx.post(url, json=task_data)
        response.raise_for_status()
        return response.json()
    
    def update_task(self, task_id, task_data):
        url = f"{self.base_url}/tasks/{task_id}"
        response = httpx.put(url, json=task_data)
        response.raise_for_status()
        return response.json()

    def delete_task(self, task_id):
        url = f"{self.base_url}/tasks/{task_id}"
        response = httpx.delete(url)
        response.raise_for_status()
        return response.json()
