from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class ReviewBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    author: str
    text: str
    rating: float = Field(..., ge=0, le=5)

class ReviewCreate(ReviewBase):
    restaurant_id: int

class ReviewResponse(ReviewBase):
    id: int
    restaurant_id: int
    created_at: datetime
    sentiment_score: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)