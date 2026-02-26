from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent.parent   # Setting up the parent directory
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
    ensure_storage(filepath)                   # Checks for json file
    with open(filepath, "r") as f:    # Loads the files
        data = json.load(f)

    return data["tasks"]    # returns the task list


def save_tasks(tasks, filepath):
    """Writes the tasks in tasks.json"""
    ensure_storage(filepath)
    with open(filepath, "w") as f:     # Opens the json file in write mode and dumps the changes in the json
        data = {"tasks":tasks}
        json.dump(data, f, indent=4)


def save_cache_json(task):
    with open(CACHE_FILE, "w") as f:
        data = {"tasks" : task}
        json.dump(data, f, indent=4)



def ensure_len(filepath, maxlen:int):  # this is for the cache file mainly
    x = load_tasks(filepath)
    if len(x) > maxlen:
        new_x = x[-maxlen:]
        save_tasks(new_x, filepath)

def update_cache():
    storage = load_tasks(TASK_FILE)
    #print(f"[DEBUG]: {storage}")
    cache = load_tasks(CACHE_FILE)
    #print(f"[DEBUG]: {cache}")

    cache.append(storage)
    #print(f"[DEBUG]: {cache}")

    '''with open(CACHE_FILE, "w") as f:
        data = {"tasks" : cache}
        json.dump(data, f, indent=4)'''
    save_cache_json(cache)




    
