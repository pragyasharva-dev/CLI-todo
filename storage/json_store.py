from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent.parent   # Setting up the parent directory
TASK_FILE = BASE_DIR / "tasks.json"                 # Setting up the json file's path


def ensure_storage():
    """Ensure tasks.json exists with valid structure."""
    if not TASK_FILE.exists():          # Creates a json file if one doesnt exist
        with open(TASK_FILE, "w") as f:
            json.dump({"tasks":[]}, f)  # Creates an empty task list as well


def load_tasks():
    """Load the contents of tasks.json"""
    ensure_storage()                   # Checks for json file
    with open(TASK_FILE, "r") as f:    # Loads the files
        data = json.load(f)

    return data["tasks"]    # returns the task list


def save_tasks(tasks):
    """Writes the tasks in tasks.json"""
    ensure_storage()
    with open(TASK_FILE, "w") as f:     # Opens the json file in write mode and dumps the changes in the json
        data = {"tasks":tasks}
        json.dump(data, f, indent=4)
    
