import sqlite3
import tempfile
import os
import sys
from pathlib import Path
import pytest

# ensure repository root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import create_schema
import generate_data

@pytest.fixture()
def temp_db(monkeypatch):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    db_path = tmp.name
    tmp.close()

    original_connect = sqlite3.connect

    def connect_override(*args, **kwargs):
        return original_connect(db_path)

    monkeypatch.setattr(create_schema.sqlite3, 'connect', connect_override)
    monkeypatch.setattr(generate_data.sqlite3, 'connect', connect_override)

    create_schema.create_tables()
    yield db_path
    os.unlink(db_path)