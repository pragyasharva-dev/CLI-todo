# CLI-todo

**Version:** 1.1.0

A command-line and graphical task manager written in Python. It allows you to manage your tasks directly from the terminal or via a GUI, with persistent storage and action-undo capabilities.

### CLI Usage

Run the program via the terminal:

```bash
python main.py <command> [arguments]
```

### GUI Usage

To launch the Graphical User Interface:

```bash
python -m GUI.app
```

### Available Commands

* **add "<task_description>"**
  Adds a new task to your list. Enclose the description in quotes if it contains spaces.
  Example: `python main.py add "Read a book"`

* **list**
  Displays all currently stored tasks along with their positions.
  Example: `python main.py list`

* **update <current_position> <new_position>**
  Changes the priority of a task by moving it from its current position to a newly specified position.
  Example: `python main.py update 3 1`

* **delete <task_index>**
  Removes a task at the specified index from the list.
  Example: `python main.py delete 2`

* **undo**
  Reverts the most recent action (such as add, delete, update, or flush).
  Example: `python main.py undo`

* **flush**
  Deletes all tasks, clearing the entire list.
  Example: `python main.py flush`

* **help**
  Displays the help guide with a list of available commands.
  Example: `python main.py help`

### Graphical Features
The newly introduced GUI provides simple interactive buttons to handle these same commands, along with specialized visual tools:
* **Priority View**: Opens a dedicated window showing tasks ordered by priority.
* **Toggle Priority**: Sets a selected task to high/low priority.
* **Toggle Completion**: Marks a submitted task as completed/uncompleted.
