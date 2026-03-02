# CLI-todo

**Version:** 1.0.0

A clean, command-line based task manager written in Python. It allows you to manage your tasks directly from the terminal with persistent storage and action-undo capabilities.

## Usage

Run the program via the terminal:

```bash
python main.py <command> [arguments]
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
