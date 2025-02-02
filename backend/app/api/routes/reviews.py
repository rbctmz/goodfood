from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...db.session import get_db
from ...db.models import Restaurant, Review
from ...schemas.review import ReviewCreate, ReviewResponse
from ...services.review_service import analyze_sentiment

router = APIRouter()

@router.post("/{restaurant_id}/reviews", response_model=ReviewResponse, status_code=201)
async def create_review(
    restaurant_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db)
):
    """Создание нового отзыва с AI-анализом"""
    try:
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        db_review = Review(
            restaurant_id=restaurant_id,
            author=review.author,
            text=review.text,
            rating=review.rating,
            sentiment_score=await analyze_sentiment(review.text)
        )
        
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{restaurant_id}/reviews", response_model=List[ReviewResponse])
async def get_restaurant_reviews(
    restaurant_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Получение отзывов о ресторане"""
    reviews = db.query(Review).filter(
        Review.restaurant_id == restaurant_id
    ).offset(skip).limit(limit).all()
    return reviews
