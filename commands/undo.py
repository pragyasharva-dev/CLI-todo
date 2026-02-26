import json
from storage.json_store import load_tasks, save_tasks, CACHE_FILE, TASK_FILE, save_cache_json

def undo_task():
    """Undo a change"""
    cache = load_tasks(CACHE_FILE)
    if not cache:
        print("Unable to undo")
        return
    latest = cache[-1]

    save_tasks(latest, TASK_FILE)
    cache.pop(-1)

    '''with open(CACHE_FILE, "w") as f:
        data = {"tasks" : cache}
        json.dump(data, f, indent=4)'''

    save_cache_json(cache)

    print("Task undo successful")







