"""Tests for models/classes.py — Task model."""
from datetime import datetime
from models.classes import Task


# ========================= Task Creation =========================

class TestTaskCreation:
    def test_default_values(self):
        """Task created with only a name should have sensible defaults."""
        task = Task("Buy groceries")
        assert task.name == "Buy groceries"
        assert task.priority is False
        assert task.completed is False
        assert isinstance(task.created_at, datetime)

    def test_custom_values(self):
        """All attributes can be explicitly set."""
        dt = datetime(2026, 1, 1, 12, 0)
        task = Task("Study", priority=True, completed=True, created_at=dt)
        assert task.name == "Study"
        assert task.priority is True
        assert task.completed is True
        assert task.created_at == dt

    def test_created_at_auto_generated(self):
        """Two tasks created sequentially should have close but distinct timestamps."""
        t1 = Task("A")
        t2 = Task("B")
        assert abs((t2.created_at - t1.created_at).total_seconds()) < 1


# ========================= Serialization =========================

class TestSerialization:
    def test_to_dict_contains_all_keys(self):
        task = Task("Test task")
        d = task.to_dict()
        assert "name" in d
        assert "priority" in d
        assert "completed" in d
        assert "created_at" in d

    def test_to_dict_datetime_is_string(self):
        """created_at should be serialized as an ISO format string."""
        task = Task("Test")
        d = task.to_dict()
        assert isinstance(d["created_at"], str)
        # Verify it can be parsed back
        datetime.fromisoformat(d["created_at"])

    def test_round_trip(self):
        """to_dict → from_dict should produce an equivalent Task."""
        original = Task("Round trip", priority=True, completed=True)
        restored = Task.from_dict(original.to_dict())
        assert restored.name == original.name
        assert restored.priority == original.priority
        assert restored.completed == original.completed
        assert restored.created_at == original.created_at

    def test_from_dict_without_created_at(self):
        """from_dict should handle a dict that has no created_at key."""
        d = {"name": "No date", "priority": False, "completed": False}
        task = Task.from_dict(d)
        assert task.name == "No date"
        assert isinstance(task.created_at, datetime)


# ========================= Toggle Methods =========================

class TestTogglePriority:
    def test_toggle_low_to_high(self):
        task = Task("T")
        assert task.priority is False
        task.toggle_priority()
        assert task.priority is True

    def test_toggle_high_to_low(self):
        task = Task("T", priority=True)
        task.toggle_priority()
        assert task.priority is False

    def test_double_toggle_returns_to_original(self):
        task = Task("T")
        task.toggle_priority()
        task.toggle_priority()
        assert task.priority is False


class TestToggleCompletion:
    def test_toggle_incomplete_to_complete(self):
        task = Task("T")
        assert task.completed is False
        task.toggle_completion()
        assert task.completed is True

    def test_toggle_complete_to_incomplete(self):
        task = Task("T", completed=True)
        task.toggle_completion()
        assert task.completed is False

    def test_double_toggle_returns_to_original(self):
        task = Task("T")
        task.toggle_completion()
        task.toggle_completion()
        assert task.completed is False
