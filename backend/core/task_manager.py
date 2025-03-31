from backend.data.storage import Storage
import logging





class TaskManager:
    def __init__(self):
        self.storage = Storage()

    def get_all_tasks(self):
        return self.storage.load_tasks()

    def add_task(self, task_data):
        logging.debug(f"Feladat hozzáadása: {task_data}")
        tasks = self.storage.load_tasks()
        task_ids = [task["id"] for task in tasks if "id" in task]
        new_id = max(task_ids, default=0) + 1
        task_data["id"] = new_id
        tasks.append(task_data)
        self.storage.save_tasks(tasks)
        logging.info(f"Új feladat hozzáadva: ID {new_id}")
        return task_data
    
    def update_task(self, task_id, updated_data):
        tasks = self.storage.load_tasks()
        for idx, task in enumerate(tasks):
            if task["id"] == task_id:
                tasks[idx].update(updated_data)
                self.storage.save_tasks(tasks)
                return tasks[idx]
        return None

    def delete_task(self, task_id):
        tasks = self.storage.load_tasks()
        tasks_after_delete = [task for task in tasks if task["id"] != task_id]
        if len(tasks) == len(tasks_after_delete):
            return False  # nem történt törlés
        self.storage.save_tasks(tasks_after_delete)
        return True  # siker
