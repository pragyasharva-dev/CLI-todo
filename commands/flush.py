from storage.json_store import TASK_FILE, ensure_len, update_cache, CACHE_FILE, MAX_LEN
import json

def flush_task_list():
    """Clear out the task list"""
    ensure_len(CACHE_FILE, MAX_LEN)
    update_cache()
    task = {'tasks':[]}                       # Simply replace the whole json with a fresh one
    with open(TASK_FILE, "w") as f:
        json.dump(task, f, indent=4)

    print("Todo list cleared!")