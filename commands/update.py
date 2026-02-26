from storage.json_store import load_tasks, save_tasks, TASK_FILE

def update_task_priority(task_no : int, desired_pos : int):
    """Updates the priority of tasks"""
    tasks = load_tasks(TASK_FILE) # Loads the tasks from json

    if not tasks:   # Checks for empty task list
        print("no task to update")
        return

    index = task_no - 1 # Adjusting the indices for operation 
    pos = desired_pos - 1

    if index < 0 or index >= len(tasks):  # Input validation
        print("Invalid task number")
        return

    if pos < 0 or pos >= len(tasks):        # Input validation
        print("Invalid destination position")
        return
    
    
    temp = tasks[index] # Storing the desired task temporarily since it will be popped later
    tasks.pop(index)    # Removing the task 
    tasks.insert(pos, temp) # Inserting the task
    

    save_tasks(tasks, TASK_FILE)  # Saving the updated changes in json

    print(f"Moved {temp} from {task_no} to {desired_pos}")


