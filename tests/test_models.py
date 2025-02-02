import sys
import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.db.models import Base, Restaurant, Location, Review, Category
from backend.app.db.session import engine

class TestModels(unittest.TestCase):
    def setUp(self):
        """Создаем тестовую БД и таблицы перед каждым тестом"""
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def tearDown(self):
        """Очищаем БД после каждого теста"""
        self.session.close()
        Base.metadata.drop_all(engine)

    def test_create_restaurant(self):
        """Тест создания ресторана"""
        restaurant = Restaurant(
            place_id="test123",
            name="Test Restaurant",
            address="Test Address",
            rating=4.5,
            price_level=2
        )
        
        self.session.add(restaurant)
        self.session.commit()

        # Проверяем, что ресторан создался
        saved_restaurant = self.session.query(Restaurant).first()
        self.assertEqual(saved_restaurant.name, "Test Restaurant")
        self.assertEqual(saved_restaurant.rating, 4.5)

    def test_create_restaurant_with_location(self):
        """Тест создания ресторана с локацией"""
        restaurant = Restaurant(
            place_id="test456",
            name="Test Restaurant with Location",
            location=Location(
                latitude=51.5074,
                longitude=-0.1278
            )
        )
        
        self.session.add(restaurant)
        self.session.commit()

        # Проверяем связи
        saved_restaurant = self.session.query(Restaurant).first()
        self.assertIsNotNone(saved_restaurant.location)
        self.assertEqual(saved_restaurant.location.latitude, 51.5074)

    def test_restaurant_categories(self):
        """Тест связи many-to-many между ресторанами и категориями"""
        category1 = Category(name="Italian")
        category2 = Category(name="Pizza")
        
        restaurant = Restaurant(
            place_id="test789",
            name="Italian Restaurant",
            categories=[category1, category2]
        )
        
        self.session.add(restaurant)
        self.session.commit()

        # Проверяем категории
        saved_restaurant = self.session.query(Restaurant).first()
        self.assertEqual(len(saved_restaurant.categories), 2)
        self.assertEqual(
            sorted([c.name for c in saved_restaurant.categories]), 
            ["Italian", "Pizza"]
        )

    def test_create_review(self):
        """Тест создания отзыва и связи с рестораном"""
        restaurant = Restaurant(
            place_id="test999",
            name="Restaurant with Review"
        )
        
        review = Review(
            restaurant=restaurant,
            author="Test User",
            rating=5.0,
            text="Great place!",
            sentiment_score=0.9
        )
        
        self.session.add(restaurant)
        self.session.add(review)
        self.session.commit()

        # Проверяем связь
        saved_restaurant = self.session.query(Restaurant).first()
        self.assertEqual(len(saved_restaurant.reviews), 1)
        self.assertEqual(saved_restaurant.reviews[0].text, "Great place!")

    def test_unique_constraints(self):
        """Тест уникальности place_id и имени категории"""
        # Создаем первый ресторан
        restaurant1 = Restaurant(
            place_id="unique123",
            name="First Restaurant"
        )
        self.session.add(restaurant1)
        self.session.commit()

        # Пробуем создать ресторан с тем же place_id
        restaurant2 = Restaurant(
            place_id="unique123",
            name="Second Restaurant"
        )
        self.session.add(restaurant2)
        
        with self.assertRaises(Exception):
            self.session.commit()
        self.session.rollback()

    def test_cascade_delete(self):
        """Тест каскадного удаления"""
        restaurant = Restaurant(
            place_id="delete_test",
            name="Restaurant to Delete",
            location=Location(
                latitude=51.5074,
                longitude=-0.1278
            )
        )
        
        self.session.add(restaurant)
        self.session.commit()

        # Удаляем ресторан
        self.session.delete(restaurant)
        self.session.commit()

        # Проверяем, что локация тоже удалилась
        location_count = self.session.query(Location).count()
        self.assertEqual(location_count, 0)

    def test_validation(self):
        """Тест валидации данных"""
        # Тест на обязательные поля
        restaurant = Restaurant(place_id="test")  # Без name
        self.session.add(restaurant)
        
        with self.assertRaises(IntegrityError):
            self.session.commit()
        self.session.rollback()

        # Тест на валидные значения рейтинга
        with self.assertRaises(ValueError):  # Изменено с Exception на ValueError
            restaurant = Restaurant(
                place_id="test",
                name="Test",
                rating=6.0  # Невалидный рейтинг
            )

        # Проверяем валидные значения
        restaurant = Restaurant(
            place_id="test",
            name="Test",
            rating=4.5  # Валидный рейтинг
        )
        self.session.add(restaurant)
        self.session.commit()
        
        saved_restaurant = self.session.query(Restaurant).first()
        self.assertEqual(saved_restaurant.rating, 4.5)

    def test_price_level_validation(self):
        """Тест валидации ценовой категории"""
        with self.assertRaises(ValueError):
            Restaurant(
                place_id="test",
                name="Test",
                price_level=5  # Невалидное значение
            )

    def test_location_validation(self):
        """Тест валидации координат"""
        with self.assertRaises(ValueError):
            Location(
                latitude=91,  # Невалидная широта
                longitude=0
            )
        
        with self.assertRaises(ValueError):
            Location(
                latitude=0,
                longitude=181  # Невалидная долгота
            )

    def test_edge_cases(self):
        """Тест граничных значений"""
        # Тест граничных значений рейтинга
        restaurant = Restaurant(
            place_id="test",
            name="Test",
            rating=5.0  # Максимальное значение
        )
        self.session.add(restaurant)
        self.session.commit()

    def test_error_handling(self):
        """Тест обработки ошибок"""
        # Тест некорректного типа данных
        with self.assertRaises(TypeError):
            Restaurant(
                place_id="test",
                name="Test",
                rating="not_a_number"
            )

if __name__ == '__main__':
    unittest.main()