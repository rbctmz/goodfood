from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class LocationBase(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class RestaurantBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    address: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    price_level: Optional[int] = Field(None, ge=0, le=4)

class RestaurantCreate(RestaurantBase):
    place_id: str
    name: str  # обязательное поле
    address: str  # обязательное поле
    price_level: int = Field(..., ge=0, le=4)  # обязательное поле
    location: Optional[LocationBase] = None

class RestaurantResponse(RestaurantBase):
    id: int
    place_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    location: Optional[LocationBase] = None
    model_config = ConfigDict(from_attributes=True)

class RestaurantFilter(BaseModel):
    cuisine: Optional[str] = None
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    max_price: Optional[int] = Field(None, ge=0, le=4)
    model_config = ConfigDict(from_attributes=True)

class ReviewBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # ... остальной код