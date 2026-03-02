from storage.json_store import load_tasks, save_tasks, TASK_FILE
from models.classes import Task


def add_task(command:str):
    task = Task(command)  # creates Task object
    tasks = load_tasks(TASK_FILE) # Checks and loads the contents of json file
    tasks.append(task)   # Adds the new task to the loaded json
    save_tasks(tasks, TASK_FILE)    # overwrites the updated task to the previous json

    print("Added task")
