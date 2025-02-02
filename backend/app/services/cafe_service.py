from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db.models import Restaurant, Category, Location
from ..schemas.restaurant import RestaurantFilter

async def get_restaurant(db: Session, restaurant_id: int) -> Optional[Restaurant]:
    """
    Получение ресторана по ID
    
    Args:
        db: SQLAlchemy сессия
        restaurant_id: ID ресторана
        
    Returns:
        Restaurant или None если не найден
    """
    return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

async def get_restaurants(
    db: Session,
    filters: RestaurantFilter,
    skip: int = 0,
    limit: int = 20
) -> List[Restaurant]:
    """Получение списка ресторанов с фильтрацией"""
    query = db.query(Restaurant)
    
    if filters.min_rating is not None:
        query = query.filter(Restaurant.rating >= filters.min_rating)
    if filters.max_price is not None:
        query = query.filter(Restaurant.price_level <= filters.max_price)
    if filters.cuisine:
        query = query.join(Restaurant.categories).filter(Category.name == filters.cuisine)
        
    return query.offset(skip).limit(limit).all()

async def create_restaurant(db: Session, data: dict) -> Restaurant:
    """Создание нового ресторана"""
    try:
        # Проверяем уникальность place_id
        exists = db.query(Restaurant).filter(Restaurant.place_id == data['place_id']).first()
        if exists:
            raise HTTPException(status_code=400, detail="Restaurant already exists")
            
        # Извлекаем данные локации
        location_data = data.pop('location', None)
        
        # Создаем ресторан
        db_restaurant = Restaurant(**data)
        db.add(db_restaurant)
        db.commit()
        db.refresh(db_restaurant)
        
        # Добавляем локацию если есть
        if location_data:
            location = Location(
                restaurant_id=db_restaurant.id,
                **location_data
            )
            db.add(location)
            db.commit()
            db.refresh(db_restaurant)
            
        return db_restaurant
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))