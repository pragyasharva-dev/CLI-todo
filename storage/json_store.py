from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent.parent
TASK_FILE = BASE_DIR / "tasks.json"


def ensure_storage():
    """Ensure tasks.json exists with valid structure."""
    if not TASK_FILE.exists():
        with open(TASK_FILE, "w") as f:
            json.dump({"tasks":[]}, f)


def load_tasks():
    """Load the contents of tasks.json"""
    ensure_storage()
    with open(TASK_FILE, "r") as f:
        data = json.load(f)

    return data["tasks"]


def save_tasks(tasks):
    """Writes the tasks in tasks.json"""
    ensure_storage()
    with open(TASK_FILE, "w") as f:
        data = {"tasks":tasks}
        json.dump(data, f, indent=4)
    
