# backend/tests/test_storage.py
from backend.data.storage import Storage
import tempfile
import os

def test_storage_save_and_load():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_file:
        tmp_path = tmp_file.name

    storage = Storage(filepath=tmp_path)
    data = [{"id": 1, "name": "Test Task"}]
    storage.save_tasks(data)

    loaded = storage.load_tasks()
    assert loaded == data

    os.remove(tmp_path)
