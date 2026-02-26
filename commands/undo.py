import json
from storage.json_store import load_tasks, save_tasks, CACHE_FILE, TASK_FILE, save_cache_json

def undo_task():
    """Undo a change"""
    cache = load_tasks(CACHE_FILE)  # loads the cache list of states
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







