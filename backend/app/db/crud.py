from sqlalchemy.orm import Session
from . import models
from ..schemas import restaurant as schemas
from typing import List, Optional

def get_restaurant(db: Session, restaurant_id: int):
    """Получение ресторана по ID"""
    return db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()

def get_restaurants(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    min_rating: Optional[float] = None,
    max_price: Optional[int] = None
) -> List[models.Restaurant]:
    """Получение списка ресторанов с фильтрацией"""
    query = db.query(models.Restaurant)
    
    if min_rating is not None:
        query = query.filter(models.Restaurant.rating >= min_rating)
    if max_price is not None:
        query = query.filter(models.Restaurant.price_level <= max_price)
        
    return query.offset(skip).limit(limit).all()

def create_restaurant(db: Session, restaurant: schemas.RestaurantCreate):
    """Создание нового ресторана"""
    db_restaurant = models.Restaurant(**restaurant.model_dump(exclude={'location'}))
    if restaurant.location:
        db_restaurant.location = models.Location(**restaurant.location.model_dump())
    
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant