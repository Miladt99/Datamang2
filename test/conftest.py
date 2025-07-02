import os
import psycopg2
import sys
import tempfile
from pathlib import Path

import pytest
from pymongo import MongoClient
from psycopg2 import connect
from testcontainers.mongodb import MongoDbContainer
from testcontainers.postgres import PostgresContainer

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

    original_connect = psycopg2.connect

    def connect_override(*args, **kwargs):
        return original_connect(db_path)

    monkeypatch.setattr(create_schema.psycopg2, 'connect', connect_override)
    monkeypatch.setattr(generate_data.psycopg2, 'connect', connect_override)

    create_schema.create_tables()
    yield db_path
    os.unlink(db_path)


@pytest.fixture(scope="session")
def postgres_container():
    """Spin up a temporary PostgreSQL container for tests."""
    with PostgresContainer("postgres:16") as postgres:
        postgres.start()
        yield postgres


@pytest.fixture()
def postgres_conn(postgres_container):
    conn = connect(postgres_container.get_connection_url())
    yield conn
    conn.close()


@pytest.fixture(scope="session")
def mongo_container():
    """Spin up a temporary MongoDB container for tests."""
    with MongoDbContainer("mongo:7") as mongo:
        mongo.start()
        yield mongo


@pytest.fixture()
def mongo_client(mongo_container):
    client = MongoClient(mongo_container.get_connection_url())
    yield client
    client.close()