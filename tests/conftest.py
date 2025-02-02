# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.db.models import Base

@pytest.fixture(scope="session")
def engine():
    """Создаем движок базы данных для тестов"""
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )

@pytest.fixture(scope="session")
def tables(engine):
    """Создаем все таблицы один раз для сессии тестирования"""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)