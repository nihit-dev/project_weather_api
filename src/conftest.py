import os
import logging

import pytest
from fastapi.testclient import TestClient

from .main import app
from .database import get_db
from .tests.test_db import override_get_db, engine
from .database import Base
from .ingest import ingest_data
from .models.weather import Weather

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def client():
    """API Client fixture"""
    test_client = TestClient(app)
    yield test_client
    Base.metadata.drop_all(bind=engine)
    delete_db()


@pytest.fixture(scope="session")
def db():
    """Database fixture"""
    db_obj = next(override_get_db())
    yield db_obj
    db_obj.close()


def delete_db():
    """Delete the test database"""
    path = os.path.join(os.curdir, "src", "tests", "test_database.db")
    path = os.path.abspath(path)

    os.remove(path)


@pytest.fixture(scope="session")
def populate_db(db):
    """Add mock data for testing"""
    try:
        if len(db.query(Weather).all()) == 0:
            curr_dir = os.curdir
            path = os.path.join(curr_dir, "src", "tests", "weather_test_data")

            path = os.path.abspath(path)
            ingest_data(path, db)
    except Exception as e:
        logging.error(f"Couldn't populate test db {e}")
