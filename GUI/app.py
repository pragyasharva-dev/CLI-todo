# --------------------- Imports ---------------------------
from tkinter import Toplevel
from storage.json_store import load_tasks, TASK_FILE
from src.task_service import add_task, delete_task, toggle_priority_command, toggle_completion_command, update_task_priority, undo_task, flush_task_list, list_task_priority
import tkinter as tk
from tkinter import simpledialog, messagebox

# ---------------------- Basic app structure -----------------------------------

root = tk.Tk()       # Create a tkinter instance, works as the entry point for the GUI
root.title("Todo App") 
root.geometry = ("400x400")   # overall app size

# ---------------------------- Function definitions ---------------------------------

def refresh_tasks():
    '''Keeps the task list live in the app'''
    task_listbox.delete(0, tk.END)   # Always clears the last task list before executing

    tasks = load_tasks(TASK_FILE)

    for i, task in enumerate(tasks, start=1):            
        task_listbox.insert(tk.END, f"{i}. {task.name}")  # Simple displaying

def add_task_gui():
    '''Adds the tasks to the task list'''
    task_text = task_entry.get().strip()   # Retrieves the task text from text field

    if not task_text:
        return

    add_task(task_text)
 
    task_entry.delete(0, tk.END)   # Clears the text field
    refresh_tasks()

def delete_task_gui():
    '''Deletes the selected task'''
    index = get_selected_index()     
    
    delete_task(index)    

    refresh_tasks()

def update_task_priority_gui():
    '''Updates the position of task in the task list'''
    index = get_selected_index()

    if not index:
        print("No task selected")     # checks for no selection

    desired = simpledialog.askinteger("Update task position", "Enter new position:")
    # opens a new pop up window that takes the desired position input

    if not desired:
        return  # User skipped the update function

    update_task_priority(index + 1, desired)  
    # index + 1 because in the main update_task function, we adjusted the index for operation

    refresh_tasks()

def undo_task_gui():
    '''Reads the cache and reverts the state'''
    undo_task()
    refresh_tasks()

def flush_task_gui():
    '''Clears the task state'''
    dialog = messagebox.askyesno("Confirm flush", "Are you sure you want to clear the Task list?")
    # confirm message
    if not dialog:
        return
    flush_task_list()
    refresh_tasks()

def priority_view_gui():
    '''Opens a tab showing the list of task in high priority task first mode'''
    tasks = list_task_priority()

    window = tk.Toplevel(root)
    window.title("Priority view")

    listbox = tk.Listbox(window)

    for i, task in enumerate(tasks, start=1):
        listbox.insert(tk.END, f"{i}. {task.name}")

    listbox.pack()

def toggle_priority_gui():
    '''Toggles the priority of a task'''
    toggle_priority_command(get_selected_index())

    task = load_tasks(TASK_FILE)[get_selected_index()]

    if task.priority == True:
        messagebox.askokcancel(title=None, message=f"{task.name} priority set to high")
    else:
        messagebox.askokcancel(title=None, message=f"{task.name} priority set to low")

def toggle_completion_gui():
    '''Mark/Unmark as completed'''
    toggle_completion_command(get_selected_index())

    task = load_tasks(TASK_FILE)[get_selected_index()]

    if task.completed == True:
        messagebox.askokcancel(title=None, message=f"{task.name} marked as completed")
    else:
        messagebox.askokcancel(title=None, message=f"{task.name} marked as uncompleted")

def get_selected_index():
    '''Fetches the actual index of the task from task list'''
    selection = task_listbox.curselection()  # returns the currently selected task, one at a time

    if not selection:
        messagebox.showwarning(title=None, message="No task selected")
        return None

    return selection[0]

def show_selected():
    '''Shows the visual index'''
    index = get_selected_index()
    print("Selected index:", index+1)

def help_task():
    """Command guide"""
    print("Available commands : help ; add ; delete ; list ; update; undo; flush")
    print("add : Takes one argument(str) and adds that as new task")
    print("delete : Takes one argument(int) and deletes the respective indexed task")
    print("list : Takes no argument and shows all the listed tasks")
    print("update : Takes two arguements(int) and updates the priority of the task")
    print("undo: Takes no argument and reverts back to the prevoius state")
    print("flush : Clears out the whole todo list(this function is also revertable using undo)")

# ----------------------- Widget definitions -------------------------------------

task_listbox = tk.Listbox(root, width=50, height=20, selectmode=tk.SINGLE)  
# Creating the widget that displays the list of tasks
task_listbox.pack(pady=20)        # padding

task_entry = tk.Entry(root, width=40)  # Creating the widget that creates the field to take input
task_entry.pack(pady=5)

# Buttons :

add_button = tk.Button(root, text="Add Task", command=add_task_gui)  
add_button.pack(pady=5)

#tk.Button(root, text="Show Selected", command=show_selected).pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", command=delete_task_gui)
delete_button.pack(pady=5)

update_button = tk.Button(root, text="Update task position", command=update_task_priority_gui)
update_button.pack(pady=5)

undo_button = tk.Button(root, text="Undo", command=undo_task_gui)
undo_button.pack(pady=5)

flush_button = tk.Button(root, text="Flush task list", command=flush_task_gui)
flush_button.pack(pady=5)

priority_view_button = tk.Button(root, text="Priority view", command=priority_view_gui)
priority_view_button.pack(pady=5)

toggle_priority = tk.Button(root, text='Toggle priority', command=toggle_priority_gui)
toggle_priority.pack(pady=5)

toggle_completion = tk.Button(root, text="Toggle completion", command=toggle_completion_gui)
toggle_completion.pack(pady=5)



# -------------------------------- Entry point ----------------------------------

refresh_tasks()
root.mainloop()