

def help_task():
    """Command guide"""
    print("Available commands : help ; add ; delete ; list ; update; undo; flush")
    print("add : Takes one argument(str) and adds that as new task")
    print("delete : Takes one argument(int) and deletes the respective indexed task")
    print("list : Takes no argument and shows all the listed tasks")
    print("update : Takes two arguements(int) and updates the priority of the task")
    print("undo: Takes no argument and reverts back to the prevoius state")
    print("flush : Clears out the whole todo list(this function is also revertable using undo)")