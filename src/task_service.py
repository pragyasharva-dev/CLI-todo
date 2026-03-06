from models.classes import Task
from storage.json_store import load_tasks, load_cache, save_tasks, save_cache_json, TASK_FILE, CACHE_FILE, MAX_LEN

# -------------------------------- Util functions -------------------------------------

def update_cache():
    """Adds the latest state in the cache list"""
    storage = load_tasks(TASK_FILE)    # loads both the json files and the cache list containing the states get appended with the current task list
    #print(f"[DEBUG]: {storage}")
    cache = load_cache(CACHE_FILE)
    #print(f"[DEBUG]: {cache}")

    cache.append(storage)
    #print(f"[DEBUG]: {cache}")

    if len(cache) >= MAX_LEN:
        cache = cache[-1:-MAX_LEN:-1] # Ensuring max length is maintained

    '''with open(CACHE_FILE, "w") as f:
        data = {"tasks" : cache}
        json.dump(data, f, indent=4)'''   # realised here that the already existing save_tasks() functions wont work here
    save_cache_json(cache)



# -------------------------------- Command functions ----------------------------------

###### Add
def add_task(command:str):
    '''Adds a task to the task list'''
    update_cache()
    task = Task(command)  # creates Task object
    tasks = load_tasks(TASK_FILE) # Checks and loads the contents of json file
    tasks.append(task)   # Adds the new task to the loaded json
    save_tasks(tasks, TASK_FILE)    # overwrites the updated task to the previous json

    print("Added task")

###### Delete
def delete_task(task_no : int):
    """Deletes a task"""
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

###### Flush
def flush_task_list():
    """Clear out the task list"""
    update_cache()
    #with open(TASK_FILE, "w") as f:
    #    json.dump(task, f, indent=4)
    save_tasks([], TASK_FILE)

    print("Todo list cleared!")

####### Priority view
def update_task_view():
    '''Creates a temporary priority based view of the task list'''
    tasks = load_tasks(TASK_FILE)

    high = []
    mid = []
    low = []

    for task in tasks:
        if task.priority == True:
            high.append(task)
        elif (task.priority == False) and (task.completed == False):
            mid.append(task)
        else:
            low.append(task)

    result = high + mid + low

    save_tasks(result, TASK_FILE)

def list_task_priority():
    tasks = load_tasks(TASK_FILE)
    high = []
    low = []

    for task in tasks:
        if task.priority == True:
            high.append(task)
        else:
            low.append(task)

    result = high+low

    #save_tasks(result, TASK_FILE)
    return result

####### List tasks
def list_task():
    """Lists all the tasks"""
    tasks = load_tasks(TASK_FILE)  # Loads the tasks from json

    if not tasks:
        print("No tasks")  # Checks for empty task list
        return

    else:
        for i, task in enumerate(tasks, start=1):  # Returns the Task number and task itself
            print(i, ".", task.name)


####### Undo
def undo_task():
    """Undo a change"""
    cache = load_cache(CACHE_FILE)  # loads the cache list of states
    if not cache:
        print("Unable to undo")     # checks for empty history
        return
    latest = cache[-1]              # extracts the last known state

    save_tasks(latest, TASK_FILE)   # replaces the latest state in the task.json
    cache.pop(-1)                   # have to remove that state from the cache ofc

    '''with open(CACHE_FILE, "w") as f:
        data = {"tasks" : cache}
        json.dump(data, f, indent=4)'''

    save_cache_json(cache)          

    print("Task undo successful")

####### Update task position
def update_task_priority(task_no : int, desired_pos : int):
    """Updates the priority of tasks"""
    update_cache()
    tasks = load_tasks(TASK_FILE) # Loads the tasks from json

    if not tasks:   # Checks for empty task list
        print("no task to update")
        return

    index = task_no - 1  # Adjusting the indices for operation 
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

    print(f"Moved {temp.name} from {task_no} to {desired_pos}")

####### Toggle priority
def toggle_priority_command(task_index):
    '''Toggles the priority of a task'''
    update_cache()
    tasks = load_tasks(TASK_FILE)
    task = tasks[task_index]
    task.toggle_priority()
    save_tasks(tasks, TASK_FILE)

####### Toggle completion status
def toggle_completion_command(task_index):
    '''Toggles the completion state'''
    update_cache()
    tasks = load_tasks(TASK_FILE)
    task = tasks[task_index]
    task.toggle_completion()
    save_tasks(tasks, TASK_FILE)


    