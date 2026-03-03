# --------------------- Imports ---------------------------
from storage.json_store import load_tasks, TASK_FILE
from commands.add import add_task
from commands.delete import delete_task
from commands.update import update_task_priority
from commands.undo import undo_task
from commands.flush import flush_task_list
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


def get_selected_index():
    '''Fetches the actual index of the task from task list'''
    selection = task_listbox.curselection()  # returns the currently selected task, one at a time

    if not selection:
        return None

    return selection[0]

def show_selected():
    '''Shows the visual index'''
    index = get_selected_index()
    print("Selected index:", index+1)

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

# -------------------------------- Entry point ----------------------------------

refresh_tasks()
root.mainloop()