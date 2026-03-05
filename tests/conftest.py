import pytest
import json
import sys
from pathlib import Path

# Ensure project root is on sys.path so imports work
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def clean_task_file(tmp_path, monkeypatch):
    """Creates a temporary tasks.json and monkeypatches TASK_FILE in both storage and task_service."""
    task_file = tmp_path / "tasks.json"
    task_file.write_text(json.dumps({"tasks": []}))

    import storage.json_store as store
    import src.task_service as service

    monkeypatch.setattr(store, "TASK_FILE", task_file)
    monkeypatch.setattr(service, "TASK_FILE", task_file)

    return task_file


@pytest.fixture
def clean_cache_file(tmp_path, monkeypatch):
    """Creates a temporary cache.json and monkeypatches CACHE_FILE in both storage and task_service."""
    cache_file = tmp_path / "cache.json"
    cache_file.write_text(json.dumps({"tasks": []}))

    import storage.json_store as store
    import src.task_service as service

    monkeypatch.setattr(store, "CACHE_FILE", cache_file)
    monkeypatch.setattr(service, "CACHE_FILE", cache_file)

    return cache_file
