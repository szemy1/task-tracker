from core.task_manager import TaskManager
import time

manager = TaskManager()
task = manager.create_task("Fejlesztés", "GUI modul")
task.start()
time.sleep(2)  # szimulált idő
task.stop()

print(task)
print("Logok:")
for log in task.logs:
    print(log)
