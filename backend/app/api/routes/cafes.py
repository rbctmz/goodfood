from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...db.session import get_db
from ...schemas.restaurant import RestaurantCreate, RestaurantResponse, RestaurantFilter
from ...services.cafe_service import create_restaurant, get_restaurant, get_restaurants

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post("/", response_model=RestaurantResponse, status_code=201)
async def create_new_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db)
):
    """Создание нового ресторана"""
    try:
        return await create_restaurant(db, restaurant.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant_by_id(restaurant_id: int, db: Session = Depends(get_db)):
    """Получение детальной информации о ресторане"""
    restaurant = await get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@router.get("/", response_model=List[RestaurantResponse])
async def search_restaurants(
    cuisine: Optional[str] = None,
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    max_price: Optional[int] = Query(None, ge=0, le=4),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Поиск ресторанов с фильтрацией"""
    try:
        filters = RestaurantFilter(
            cuisine=cuisine,
            min_rating=min_rating,
            max_price=max_price
        )
        restaurants = await get_restaurants(db, filters, skip, limit)
        return restaurants or []
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.options("/")
async def cors_handler():
    """Обработчик CORS preflight запросов"""
    return {
        "access-control-allow-origin": "*",
        "access-control-allow-methods": "GET, POST, PUT, DELETE, OPTIONS",
        "access-control-allow-headers": "*"
    }