from storage.json_store import load_tasks, save_tasks, TASK_FILE
#from models.classes import Task

def delete_task(task_no : int):
    """Deletes a task"""
    tasks = load_tasks(TASK_FILE)  # Loads the tasks from json
    
    if not tasks:
        print("No tasks to delete")  # Checks for empty task list
        return

    index = task_no - 1   # Adjusting the index for operation
    
    if index < 0 or index >= len(tasks):
        print("Invalid index")             # Input validation
        return

    removed = tasks.pop(index)   # Delete the task
    
    save_tasks(tasks, TASK_FILE)    # Save the changes in the json
        
    print(f"Deleted: {removed.name}")
