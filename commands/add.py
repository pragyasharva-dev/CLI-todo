from storage.json_store import load_tasks, save_tasks, TASK_FILE, CACHE_FILE, MAX_LEN, ensure_len, update_cache
from models.classes import Task


def add_task(command:str):
    ensure_len(CACHE_FILE, MAX_LEN)
    update_cache()
    task = Task(command)  # creates Task object
    tasks = load_tasks(TASK_FILE) # Checks and loads the contents of json file
    tasks.append(task)   # Adds the new task to the loaded json
    save_tasks(tasks, TASK_FILE)    # overwrites the updated task to the previous json

    print("Added task")
