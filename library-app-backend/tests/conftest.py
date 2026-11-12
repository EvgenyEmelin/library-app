import os
import subprocess
import sys
from pathlib import Path

import pytest
from core.config import settings
from db.session import create_engine, get_db
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import sessionmaker

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

TEST_DB_NAME = "library_test"
TEST_DATABASE_URL = (
    f"postgresql+psycopg://{settings.db_user}:"
    f"{settings.db_password.get_secret_value()}@"
    f"{settings.db_host}:{settings.db_port}/{TEST_DB_NAME}"
)

test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)

@pytest.fixture(scope='session', autouse=True)
def apply_migrations():
    env = {**os.environ, "DATABASE_URL": TEST_DATABASE_URL}
    subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=BACKEND_DIR,
        env=env,
        check=True,
    )
    yield
    subprocess.run(
        [sys.executable, "-m", "alembic", "downgrade", "base"],
        cwd=BACKEND_DIR,
        env=env,
        check=True,
    )


@pytest.fixture(scope='session')
def engine():
    env = {**os.environ, "DATABASE_URL": TEST_DATABASE_URL}
    subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=BACKEND_DIR,
        env=env,
        check=True,
    )

    db_engine = create_engine(TEST_DATABASE_URL)
    yield db_engine

    db_engine.dispose()
    subprocess.run(
        [sys.executable, "-m", "alembic", "downgrade", "base"],
        cwd=BACKEND_DIR,
        env=env,
        check=True,
    )

@pytest.fixture(scope='function')
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(connection)
    session = SessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope='function')
def client():
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()