from storage.json_store import load_tasks, TASK_FILE
#from models.classes import Task


def list_task():
    """Lists all the tasks"""
    tasks = load_tasks(TASK_FILE)  # Loads the tasks from json

    if not tasks:
        print("No tasks")  # Checks for empty task list
        return

    else:
        for i, task in enumerate(tasks, start=1):  # Returns the Task number and task itself
            print(i, ".", task.name)
