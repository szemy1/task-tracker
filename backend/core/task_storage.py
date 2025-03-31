class TaskStorage:
    def __init__(self):
        self._tasks = []

    def set_tasks(self, tasks):
        self._tasks = tasks

    def get_task_by_id(self, task_id: int):
        for task in self._tasks:
            if task["id"] == task_id:
                return task
        return None

# Globális példány
task_storage = TaskStorage()
