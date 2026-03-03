from storage.json_store import load_tasks, save_tasks, TASK_FILE, CACHE_FILE, MAX_LEN, ensure_len, update_cache
#from models.classes import Task

def delete_task(task_no : int):
    """Deletes a task"""
    ensure_len(CACHE_FILE, MAX_LEN)
    update_cache()
    tasks = load_tasks(TASK_FILE)  # Loads the tasks from json
    
    if not tasks:
        print("No tasks to delete")  # Checks for empty task list
        return

    index = task_no   # Adjustment not required anymore since we using original index in GUI
    
    if index < 0 or index >= len(tasks):
        print("Invalid index")             # Input validation
        return

    removed = tasks.pop(index)   # Delete the task
    
    save_tasks(tasks, TASK_FILE)    # Save the changes in the json
        
    print(f"Deleted: {removed.name}")
