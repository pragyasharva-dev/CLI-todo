"""Tests for storage/json_store.py — JSON persistence layer."""
import json
from pathlib import Path
from models.classes import Task
from storage.json_store import (
    ensure_storage,
    load_tasks,
    save_tasks,
    load_cache,
    save_cache_json,
    ensure_len,
)


# ========================= ensure_storage =========================

class TestEnsureStorage:
    def test_creates_file_when_missing(self, tmp_path):
        """Should create a valid JSON file if it doesn't exist."""
        filepath = tmp_path / "new.json"
        assert not filepath.exists()
        ensure_storage(filepath)
        assert filepath.exists()
        data = json.loads(filepath.read_text())
        assert data == {"tasks": []}

    def test_repairs_invalid_json(self, tmp_path):
        """Should overwrite corrupted JSON with a valid empty structure."""
        filepath = tmp_path / "bad.json"
        filepath.write_text("{invalid json content!!")
        ensure_storage(filepath)
        data = json.loads(filepath.read_text())
        assert data == {"tasks": []}

    def test_leaves_valid_file_intact(self, tmp_path):
        """Should not overwrite a file that already has valid JSON."""
        filepath = tmp_path / "valid.json"
        original = {"tasks": [{"name": "Keep me", "priority": False, "completed": False, "created_at": "2026-01-01T00:00:00"}]}
        filepath.write_text(json.dumps(original))
        ensure_storage(filepath)
        data = json.loads(filepath.read_text())
        assert data == original


# ========================= load_tasks / save_tasks =========================

class TestLoadSaveTasks:
    def test_save_and_load_single_task(self, clean_task_file):
        """Save one task, load it back, and verify attributes."""
        task = Task("Test task")
        save_tasks([task], clean_task_file)
        loaded = load_tasks(clean_task_file)
        assert len(loaded) == 1
        assert loaded[0].name == "Test task"
        assert loaded[0].priority is False
        assert loaded[0].completed is False

    def test_save_and_load_multiple_tasks(self, clean_task_file):
        """Multiple tasks should round-trip correctly."""
        tasks = [Task("A"), Task("B", priority=True), Task("C", completed=True)]
        save_tasks(tasks, clean_task_file)
        loaded = load_tasks(clean_task_file)
        assert len(loaded) == 3
        assert loaded[0].name == "A"
        assert loaded[1].priority is True
        assert loaded[2].completed is True

    def test_load_empty_file(self, clean_task_file):
        """Loading from an empty tasks.json should return an empty list."""
        loaded = load_tasks(clean_task_file)
        assert loaded == []

    def test_save_empty_list(self, clean_task_file):
        """Saving an empty list should produce a valid empty file."""
        save_tasks([], clean_task_file)
        loaded = load_tasks(clean_task_file)
        assert loaded == []

    def test_task_attributes_persist(self, clean_task_file):
        """Priority, completion, and created_at should survive save/load."""
        from datetime import datetime
        dt = datetime(2026, 6, 15, 10, 30)
        task = Task("Important", priority=True, completed=True, created_at=dt)
        save_tasks([task], clean_task_file)
        loaded = load_tasks(clean_task_file)
        assert loaded[0].priority is True
        assert loaded[0].completed is True
        assert loaded[0].created_at == dt


# ========================= load_cache / save_cache_json =========================

class TestCachePersistence:
    def test_save_and_load_cache(self, clean_cache_file, monkeypatch):
        """Cache stores a list of task-list snapshots (nested structure)."""
        import storage.json_store as store
        monkeypatch.setattr(store, "CACHE_FILE", clean_cache_file)

        snapshot1 = [Task("A"), Task("B")]
        snapshot2 = [Task("A"), Task("B"), Task("C")]
        save_cache_json([snapshot1, snapshot2])

        loaded = load_cache(clean_cache_file)
        assert len(loaded) == 2
        assert len(loaded[0]) == 2
        assert len(loaded[1]) == 3
        assert loaded[1][2].name == "C"

    def test_empty_cache(self, clean_cache_file):
        """Loading an empty cache should return an empty list."""
        loaded = load_cache(clean_cache_file)
        assert loaded == []


# ========================= ensure_len =========================

class TestEnsureLen:
    def test_trims_cache_when_over_max(self, clean_cache_file, monkeypatch):
        """Cache should be trimmed to stay within MAX_LEN."""
        import storage.json_store as store
        monkeypatch.setattr(store, "CACHE_FILE", clean_cache_file)

        # Create 6 snapshots, MAX_LEN is 5
        snapshots = [[Task(f"Task {i}")] for i in range(6)]
        save_cache_json(snapshots)

        ensure_len(clean_cache_file, 5)
        loaded = load_cache(clean_cache_file)
        assert len(loaded) < 6

    def test_no_trim_when_under_max(self, clean_cache_file, monkeypatch):
        """Cache should not be modified if it's under MAX_LEN."""
        import storage.json_store as store
        monkeypatch.setattr(store, "CACHE_FILE", clean_cache_file)

        snapshots = [[Task("A")], [Task("B")]]
        save_cache_json(snapshots)

        ensure_len(clean_cache_file, 5)
        loaded = load_cache(clean_cache_file)
        assert len(loaded) == 2
