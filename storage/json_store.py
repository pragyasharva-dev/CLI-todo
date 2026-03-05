from models.classes import Task
from pathlib import Path
import os
import json

APP_NAME = "TodoApp"
BASE_DIR = Path(os.getenv("LOCALAPPDATA")) / APP_NAME
BASE_DIR.mkdir(parents=True, exist_ok=True)

TASK_FILE = BASE_DIR / "tasks.json"                 # Setting up the task storage json file's path
CACHE_FILE = BASE_DIR / "cache.json"                # Setting up the cache memory json file's path
MAX_LEN = 5


def ensure_storage(filepath):
    """Ensure tasks.json exists with valid structure."""
    if not filepath.exists():          # Creates a json file if one doesnt exist
        with open(filepath, "w") as f:
            json.dump({"tasks":[]}, f)  # Creates an empty task list as well

    try:
        with open(filepath, "r") as f:
            json.load(f)
    except json.JSONDecodeError:
        with open(filepath, "w") as f:
            json.dump({"tasks":[]}, f)


def load_tasks(filepath):
    """Load the contents of tasks.json"""
    ensure_storage(filepath)
    result = []                       # Checks for json file
    with open(filepath, "r") as f:    # Loads the files
        data = json.load(f)

    for i in data["tasks"]:
        result.append(Task.from_dict(i))

    return result    # returns the task list

def load_cache(filepath):
    '''Loads the cache task list'''
    ensure_storage(filepath)
    cache = []
    with open(filepath, "r") as f:
        data = json.load(f)
    for i in data["tasks"]:  # iterates through the states
        task = []           # creates empty list to store the task state of the current iteration
        for j in i:            
            task.append(Task.from_dict(j))  # goes through the dictionaries in the current states, converts them into Task objects and appends in the empty task list
        cache.append(task)      # appends all the lists of Task objects
    
    return cache
    


def save_tasks(tasks , filepath):
    """Overwrites the tasks in tasks.json"""
    ensure_storage(filepath)
    result = []
    for item in tasks:
        result.append(item.to_dict())
    with open(filepath, "w") as f:     # Opens the json file in write mode and dumps the changes in the json
        data = {"tasks":result}
        json.dump(data, f, indent=4)


def save_cache_json(tasks):
    """Cache stores raw task list, not wrapped structure"""
    cache = []
    for item in tasks:   
        task = []
        for j in item:                    # same logic as load_cache()
            task.append(j.to_dict())
        cache.append(task)
    with open(CACHE_FILE, "w") as f:
        data = {"tasks" : cache}
        json.dump(data, f, indent=4)



def ensure_len(filepath, maxlen:int):  # this is for the cache file mainly
    """Ensures that the length of the cache list doesnt exceed max length"""
    x = load_cache(filepath)            
    #print("[DEBUG]: ", len(x))
    if len(x) >= maxlen:
        new_x = x[-1:-maxlen:-1]       # fixed error, wasnt working earlier because of slicing error
        #print(f"[DEBUG] : {new_x}")
        save_cache_json(new_x[::-1])   # used save_tasks earlier which was showing error because of differences in storing methods

def update_cache():
    """Adds the latest state in the cache list"""
    storage = load_tasks(TASK_FILE)    # loads both the json files and the cache list containing the states get appended with the current task list
    #print(f"[DEBUG]: {storage}")
    cache = load_cache(CACHE_FILE)
    #print(f"[DEBUG]: {cache}")

    cache.append(storage)
    #print(f"[DEBUG]: {cache}")

    '''with open(CACHE_FILE, "w") as f:
        data = {"tasks" : cache}
        json.dump(data, f, indent=4)'''   # realised here that the already existing save_tasks() functions wont work here
    save_cache_json(cache)




    
