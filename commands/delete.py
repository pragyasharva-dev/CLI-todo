from storage.json_store import load_tasks, save_tasks

def delete_task(task_no : int):
    tasks = load_tasks()
    
    if not tasks:
        print("No tasks to delete")
        return

    index = task_no - 1
    
    if index < 0 or index >= len(tasks):
        print("Invalid index")
        return

    removed = tasks.pop(index)
    
    save_tasks(tasks)
        
    print(f"Deleted: {removed}")
