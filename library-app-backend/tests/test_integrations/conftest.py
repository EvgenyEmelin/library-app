import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from models.book import BookORM
from repository.book import BookRepository
from service.book import BookService
from sqlalchemy.orm import Session, sessionmaker

# Добавляем корень бэкенда в sys.path ДО импорта внутренних модулей
BACKEND_DIR = Path(__file__).resolve().parents
sys.path.insert(0, str(BACKEND_DIR))

from core.config import settings
from db.session import create_engine, get_db
from main import app
from models.book import Base

# Страховка: не даем тестам запуститься, если .test.env не подхватился
assert "test" in settings.db_name.lower(), (
    f"ОПАСНОСТЬ! Тесты пытаются запуститься на нетестовой БД: {settings.db_name}"
)

TEST_DATABASE_URL = (
    f"postgresql+psycopg://{settings.db_user}:"
    f"{settings.db_password.get_secret_value()}@"
    f"{settings.db_host}:{settings.db_port}/{settings.db_name}"
)


@pytest.fixture(scope="session")
def engine():
    db_engine = create_engine(TEST_DATABASE_URL)

    # Создаем таблицы перед прогоном всех тестов
    Base.metadata.create_all(bind=db_engine)

    yield db_engine

    # Удаляем таблицы после завершения тестов и закрываем пул соединений
    Base.metadata.drop_all(bind=db_engine)
    db_engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    yield session

    session.close()
    # Откатываем транзакцию только если она еще активна
    if transaction.is_active:
        transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def repo(db_session: Session) -> BookRepository:
    return BookRepository(db_session)

@pytest.fixture
def service(db_session: Session) -> BookService:
    return BookService(db_session)
