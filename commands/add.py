from storage.json_store import load_tasks, save_tasks


def add_task(task:str):
    tasks = load_tasks() # Checks and loads the contents of json file
    tasks.append(task)   # Adds the new task to the loaded json
    save_tasks(tasks)    # overwrites the updated task to the previous json

    print("Added task")
