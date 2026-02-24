from storage.json_store import load_tasks


def list_task():
    tasks = load_tasks()
    if not tasks:
        print("No tasks")
        return

    else:
        for i, task in enumerate(tasks, start=1):
            print(i, ".", task)
