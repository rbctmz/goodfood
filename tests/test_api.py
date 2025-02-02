import pytest
from pytest import fixture
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from datetime import datetime
from sqlalchemy.pool import StaticPool
from unittest.mock import patch, MagicMock
from httpx import AsyncClient, ASGITransport


# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.db.models import Base, Restaurant, Location
from backend.app.db.session import get_db
from backend.app.main import app
from backend.app.services.review_service import analyze_sentiment


# Создаем тестовую БД
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_test_db():
    """Синхронная версия get_db для тестов"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    """Создаем таблицы перед каждым тестом"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Создаем тестовую сессию
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_db():
    """Фикстура для доступа к тестовой БД"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def sample_restaurant():
    """Фикстура с тестовыми данными ресторана"""
    return {
        "place_id": "test123",
        "name": "Test Restaurant",
        "address": "Test Address",
        "rating": 4.5,
        "price_level": 2,
        "location": {
            "latitude": 51.5074,
            "longitude": -0.1278
        }
    }

@pytest.fixture
def valid_restaurant_data():
    """Фикстура с валидными данными ресторана"""
    return {
        "place_id": "test123",
        "name": "Test Restaurant",
        "address": "Test Address",
        "rating": 4.5,
        "price_level": 2,
        "location": {
            "latitude": 51.5074,
            "longitude": -0.1278
        }
    }

def test_create_restaurant(valid_restaurant_data):
    """Тест создания ресторана через API"""
    response = client.post("/restaurants/", json=valid_restaurant_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == valid_restaurant_data["name"]
    assert "id" in data

def test_get_restaurant(test_db):
    """Тест получения информации о ресторане"""
    restaurant_data = {
        "place_id": "test456",
        "name": "Test Restaurant",
        "address": "Test Address",
        "rating": 4.5,
        "price_level": 2,
        "location": {
            "latitude": 51.5074,
            "longitude": -0.1278
        }
    }
    response = client.post("/restaurants/", json=restaurant_data)
    assert response.status_code == 201
    data = response.json()
    restaurant_id = data["id"]
    
    # Получаем информацию о созданном ресторане
    response = client.get(f"/restaurants/{restaurant_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == restaurant_data["name"]

def test_search_restaurants(valid_restaurant_data):
    """Тест поиска ресторанов с фильтрами"""
    # Создаем тестовый ресторан
    response = client.post("/restaurants/", json=valid_restaurant_data)
    assert response.status_code == 201

    # Поиск без фильтров (только пагинация)
    response = client.get(
        "/restaurants/",  # Изменили путь с /search на /
        params={"skip": 0, "limit": 10}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Поиск с фильтром по рейтингу
    test_rating = valid_restaurant_data["rating"] - 0.1
    response = client.get(
        "/restaurants/",  # Изменили путь с /search на /
        params={
            "min_rating": test_rating,
            "skip": 0,
            "limit": 10
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(r["rating"] >= test_rating for r in data)

def test_restaurant_validation():
    """Тест валидации данных ресторана"""
    invalid_restaurant = {
        "place_id": "test789",
        "name": "Invalid Restaurant",
        "rating": 6.0  # Невалидный рейтинг
    }
    
    response = client.post("/restaurants/", json=invalid_restaurant)
    assert response.status_code == 422

def test_error_handling(valid_restaurant_data):
    """Тест обработки ошибок"""
    # Тест несуществующего ресторана
    response = client.get("/restaurants/999")
    assert response.status_code == 404
    
    # Тест дубликата place_id
    response = client.post("/restaurants/", json=valid_restaurant_data)
    assert response.status_code == 201
    
    # Повторное создание с тем же place_id
    response = client.post("/restaurants/", json=valid_restaurant_data)
    assert response.status_code == 400

def test_cors():
    """Тест CORS заголовков"""
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type"
    }
    response = client.options("/restaurants/", headers=headers)
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers

def test_crud_operations(test_db):
    """Тест CRUD операций с ресторанами"""
    # Создание
    restaurant_data = {
        "place_id": "crud_test",
        "name": "CRUD Test Restaurant",
        "address": "Test Address",
        "rating": 4.5,
        "price_level": 2
    }
    response = client.post("/restaurants/", json=restaurant_data)
    created_id = response.json()["id"]
    
    # Чтение
    response = client.get(f"/restaurants/{created_id}")
    assert response.status_code == 200
    assert response.json()["name"] == restaurant_data["name"]
    
    # Обновление фильтров поиска
    response = client.get("/restaurants/", params={
        "min_rating": 4.0,
        "max_price": 3
    })
    assert response.status_code == 200
    
    # Проверка несуществующего ресторана
    response = client.get("/restaurants/9999")
    assert response.status_code == 404

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_review_sentiment(async_client):
    """Тест анализа тональности отзыва"""
    # Создаем тестовый ресторан
    restaurant_data = {
        "place_id": "test123", 
        "name": "Test Restaurant",
        "address": "Test Address",
        "rating": 4.5,
        "price_level": 2,
        "location": {
            "latitude": 51.5074,
            "longitude": -0.1278
        }
    }
    
    response = await async_client.post("/restaurants/", json=restaurant_data)
    assert response.status_code == 201
    data = response.json()
    restaurant_id = data["id"]
    
    # Создаем отзыв
    review_data = {
        "restaurant_id": restaurant_id,
        "author": "Test User",
        "text": "Great place!",
        "rating": 5.0
    }
    
    response = await async_client.post(
        f"/restaurants/{restaurant_id}/reviews",
        json=review_data
    )
    
    assert response.status_code == 201
    review = response.json()
    assert "sentiment_score" in review
    assert isinstance(review["sentiment_score"], float)

@pytest.mark.asyncio
async def test_reviews_api(async_client):
    """Тест API отзывов"""
    # Создаем тестовый ресторан
    restaurant_data = {
        "place_id": "test123",
        "name": "Test Restaurant",
        "address": "Test Address",
        "rating": 4.5,
        "price_level": 2,
        "location": {
            "latitude": 51.5074,
            "longitude": -0.1278
        }
    }
    
    response = await async_client.post("/restaurants/", json=restaurant_data)
    assert response.status_code == 201
    data = response.json()
    restaurant_id = data["id"]
    
    # Создаем отзыв
    review_data = {
        "restaurant_id": restaurant_id,
        "author": "Test User",
        "text": "Great place!",
        "rating": 5.0
    }
    
    response = await async_client.post(
        f"/restaurants/{restaurant_id}/reviews",
        json=review_data
    )
    assert response.status_code == 201
    assert "sentiment_score" in response.json()
