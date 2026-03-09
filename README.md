# CLI-todo & TodoApp GUI

**Version:** 2.0.5

A powerful, dual-interface task manager written in Python. It allows you to manage your tasks at lighting speed from your terminal, or through a beautiful, fully-themed Graphical User Interface with persistent storage and action-undo capabilities.

### ⬇️ Download

You can download the compiled Windows executable directly. **It includes an Auto-Updater**, so you'll never fall behind!
**[Download TodoApp.exe](https://github.com/pragyasharva-dev/CLI-todo/releases/latest/download/TodoApp.exe)**

---

### 📝 Patch Notes (v2.0.1)
* **Bug Fix:** Fixed an issue where the priority sorting view (`update_task_view`) ordered High Priority tasks to the bottom of the list.
* **Bug Fix:** Secured the caching mechanism for the Undo tool to ensure that invalid or aborted actions no longer clog the memory history.
* **Enhancement:** Added intensive multi-state undo memory tracking and test coverage natively within Pytest.
* **Enhancement:** Corrected GUI asset pathing so PyInstaller can accurately bundle custom background themes and window icons into the `TodoApp.exe` standalone file.

### 🎨 Graphical Features (v2.0.0 Update)
The entire GUI has been overhauled using **PyQt6** to provide a smooth, modern, and highly customizable experience:
* **Rich Themes:** Instantly switch between custom palettes: *Dark, Light, Hacker, Ocean, Sunset, Nature, and Cute*.
* **Custom Backgrounds:** Selected themes feature full-image background support with glass-morphic transparencies.
* **Drag-and-Drop:** Intuitive task reordering. Just click and drag a task to change its priority order!
* **Quick Actions:**
  * Click the `☆` star next to a task to toggle High Priority.
  * Click the `☐` checkbox to mark a task as completed (auto-moves to bottom with strikethrough).
* **Auto-Updater:** The application checks GitHub for updates silently in the background and prompts you to install them with one click.
* **Theme Persistence:** The app remembers your selected theme and automatically loads it next time.
* **Safety First:** Confirmation pop-ups prevent accidental task deletion or clearing.

### 💻 CLI Usage

Run the program via the terminal:

```bash
python main.py <command> [arguments]
```

#### Available Commands:
* **add "<task_description>"** - Adds a new task.
* **list** - Displays all currently stored tasks.
* **update <current_position> <new_position>** - Changes task priority/position.
* **delete <task_index>** - Removes a task.
* **undo** - Reverts the most recent action (add, delete, update, or flush).
* **flush** - Deletes all tasks, clearing the entire list.
* **help** - Displays the help guide.
