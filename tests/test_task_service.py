"""Tests for src/task_service.py — command/service layer."""
from models.classes import Task
from storage.json_store import load_tasks, save_tasks, load_cache, save_cache_json
from src.task_service import (
    add_task,
    delete_task,
    flush_task_list,
    undo_task,
    update_task_priority,
    list_task_priority,
    toggle_priority_command,
    toggle_completion_command,
)


# ========================= add_task =========================

class TestAddTask:
    def test_add_single_task(self, clean_task_file, clean_cache_file):
        """Adding a task should persist it in tasks.json."""
        add_task("Buy milk")
        tasks = load_tasks(clean_task_file)
        assert len(tasks) == 1
        assert tasks[0].name == "Buy milk"

    def test_add_multiple_tasks(self, clean_task_file, clean_cache_file):
        """Tasks should accumulate in order."""
        add_task("Task A")
        add_task("Task B")
        add_task("Task C")
        tasks = load_tasks(clean_task_file)
        assert len(tasks) == 3
        assert tasks[0].name == "Task A"
        assert tasks[2].name == "Task C"

    def test_add_preserves_existing(self, clean_task_file, clean_cache_file):
        """Adding a new task should not remove existing ones."""
        save_tasks([Task("Existing")], clean_task_file)
        add_task("New")
        tasks = load_tasks(clean_task_file)
        assert len(tasks) == 2
        assert tasks[0].name == "Existing"
        assert tasks[1].name == "New"


# ========================= delete_task =========================

class TestDeleteTask:
    def test_delete_valid_index(self, clean_task_file, clean_cache_file):
        """Deleting by valid index should remove that task."""
        save_tasks([Task("A"), Task("B"), Task("C")], clean_task_file)
        delete_task(1)  # delete "B" (0-indexed)
        tasks = load_tasks(clean_task_file)
        assert len(tasks) == 2
        assert tasks[0].name == "A"
        assert tasks[1].name == "C"

    def test_delete_first_task(self, clean_task_file, clean_cache_file):
        """Deleting index 0 should remove the first task."""
        save_tasks([Task("First"), Task("Second")], clean_task_file)
        delete_task(0)
        tasks = load_tasks(clean_task_file)
        assert len(tasks) == 1
        assert tasks[0].name == "Second"

    def test_delete_invalid_index(self, clean_task_file, clean_cache_file, capsys):
        """Deleting an out-of-range index should print an error and leave tasks unchanged."""
        save_tasks([Task("Only")], clean_task_file)
        delete_task(5)
        tasks = load_tasks(clean_task_file)
        assert len(tasks) == 1
        captured = capsys.readouterr()
        assert "Invalid index" in captured.out

    def test_delete_from_empty_list(self, clean_task_file, clean_cache_file, capsys):
        """Deleting from an empty list should print a message."""
        delete_task(0)
        captured = capsys.readouterr()
        assert "No tasks to delete" in captured.out


# ========================= flush_task_list =========================

class TestFlushTaskList:
    def test_flush_clears_all(self, clean_task_file, clean_cache_file):
        """Flushing should result in an empty task list."""
        save_tasks([Task("A"), Task("B")], clean_task_file)
        flush_task_list()
        tasks = load_tasks(clean_task_file)
        assert len(tasks) == 0

    def test_flush_empty_list(self, clean_task_file, clean_cache_file):
        """Flushing an already empty list should not error."""
        flush_task_list()
        tasks = load_tasks(clean_task_file)
        assert len(tasks) == 0


# ========================= undo_task =========================

class TestUndoTask:
    def test_undo_reverts_state(self, clean_task_file, clean_cache_file, monkeypatch):
        """Undo should restore the task list to its previous state."""
        import storage.json_store as store
        monkeypatch.setattr(store, "CACHE_FILE", clean_cache_file)

        # Manually set up: cache has one previous state [Task("A")]
        previous_state = [Task("A")]
        save_cache_json([previous_state])

        # Current tasks are different
        save_tasks([Task("A"), Task("B")], clean_task_file)

        undo_task()

        tasks = load_tasks(clean_task_file)
        assert len(tasks) == 1
        assert tasks[0].name == "A"

    def test_undo_empty_cache(self, clean_task_file, clean_cache_file, capsys):
        """Undo with no history should print a warning."""
        undo_task()
        captured = capsys.readouterr()
        assert "Unable to undo" in captured.out


# ========================= update_task_priority =========================

class TestUpdateTaskPriority:
    def test_move_task_position(self, clean_task_file, clean_cache_file):
        """Moving task from position 3 to position 1 should reorder."""
        save_tasks([Task("A"), Task("B"), Task("C")], clean_task_file)
        update_task_priority(3, 1)  # move "C" to position 1 (1-indexed)
        tasks = load_tasks(clean_task_file)
        assert tasks[0].name == "C"
        assert tasks[1].name == "A"
        assert tasks[2].name == "B"

    def test_invalid_task_number(self, clean_task_file, clean_cache_file, capsys):
        """Invalid source index should print an error."""
        save_tasks([Task("A")], clean_task_file)
        update_task_priority(5, 1)
        captured = capsys.readouterr()
        assert "Invalid task number" in captured.out

    def test_invalid_destination(self, clean_task_file, clean_cache_file, capsys):
        """Invalid destination position should print an error."""
        save_tasks([Task("A"), Task("B")], clean_task_file)
        update_task_priority(1, 10)
        captured = capsys.readouterr()
        assert "Invalid destination position" in captured.out

    def test_update_empty_list(self, clean_task_file, clean_cache_file, capsys):
        """Updating on an empty list should print a message."""
        update_task_priority(1, 1)
        captured = capsys.readouterr()
        assert "no task to update" in captured.out


# ========================= list_task_priority =========================

class TestListTaskPriority:
    def test_high_priority_first(self, clean_task_file, clean_cache_file):
        """High priority tasks should appear before low priority ones."""
        tasks = [
            Task("Low1"),
            Task("High1", priority=True),
            Task("Low2"),
            Task("High2", priority=True),
        ]
        save_tasks(tasks, clean_task_file)
        result = list_task_priority()
        assert result[0].name == "High1"
        assert result[1].name == "High2"
        assert result[2].name == "Low1"
        assert result[3].name == "Low2"

    def test_all_same_priority(self, clean_task_file, clean_cache_file):
        """Tasks with the same priority should maintain their original order."""
        tasks = [Task("A"), Task("B"), Task("C")]
        save_tasks(tasks, clean_task_file)
        result = list_task_priority()
        assert [t.name for t in result] == ["A", "B", "C"]

    def test_empty_list(self, clean_task_file, clean_cache_file):
        """Priority view on empty list should return empty."""
        result = list_task_priority()
        assert result == []


# ========================= toggle_priority_command =========================

class TestTogglePriorityCommand:
    def test_toggle_on(self, clean_task_file, clean_cache_file):
        """Toggling a low-priority task should make it high."""
        save_tasks([Task("A")], clean_task_file)
        toggle_priority_command(0)
        tasks = load_tasks(clean_task_file)
        assert tasks[0].priority is True

    def test_toggle_off(self, clean_task_file, clean_cache_file):
        """Toggling a high-priority task should make it low."""
        save_tasks([Task("A", priority=True)], clean_task_file)
        toggle_priority_command(0)
        tasks = load_tasks(clean_task_file)
        assert tasks[0].priority is False


# ========================= toggle_completion_command =========================

class TestToggleCompletionCommand:
    def test_toggle_complete(self, clean_task_file, clean_cache_file):
        """Toggling an incomplete task should mark it complete."""
        save_tasks([Task("A")], clean_task_file)
        toggle_completion_command(0)
        tasks = load_tasks(clean_task_file)
        assert tasks[0].completed is True

    def test_toggle_uncomplete(self, clean_task_file, clean_cache_file):
        """Toggling a completed task should mark it incomplete."""
        save_tasks([Task("A", completed=True)], clean_task_file)
        toggle_completion_command(0)
        tasks = load_tasks(clean_task_file)
        assert tasks[0].completed is False
