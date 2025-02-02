import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.db.models import Base, Restaurant, Location
from backend.app.db import crud
from backend.app.schemas.restaurant import RestaurantCreate

# Создаем тестовую in-memory БД
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Перед запуском тестов создаем таблицы
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    """
    Фикстура для получения сессии тестовой БД.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_restaurant(db):
    """
    Тестирует функцию создания ресторана.
    """
    # Данные нового ресторана должны соответствовать схеме RestaurantCreate.
    restaurant_data = {
        "place_id": "test_create",
        "name": "Test Create",
        "address": "Test Address",
        "rating": 4.0,
        "price_level": 2,
        "location": {
        "latitude": 40.0,
        "longitude": -70.0
        }
    }
    # Создаем объект схемы RestaurantCreate
    restaurant_create = RestaurantCreate(**restaurant_data)
    # Вызываем функцию создания ресторана
    new_restaurant = crud.create_restaurant(db, restaurant_create)
    # Проверяем, что у созданного объекта есть идентификатор и имя совпадает с ожидаемым
    assert new_restaurant.id is not None
    assert new_restaurant.name == "Test Create"
    # Если в модели предусмотрено создание связанной локации, можно проверить и её наличие:
    if restaurant_data.get("location"):
        assert new_restaurant.location is not None
        assert new_restaurant.location.latitude == 40.0
    else:
        # Если связанная локация не предусмотрена в модели, то проверить ее наличие можно также по атрибуту "location":
        assert new_restaurant.location is not None

