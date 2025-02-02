from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, declarative_base, validates
from datetime import datetime

Base = declarative_base()

# Связующая таблица для категорий
restaurant_categories = Table(
    'restaurant_categories',
    Base.metadata,
    Column('restaurant_id', Integer, ForeignKey('restaurants.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class Restaurant(Base):
    __tablename__ = 'restaurants'
    
    id = Column(Integer, primary_key=True)
    place_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String)
    rating = Column(Float)
    price_level = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    location = relationship(
        "Location", 
        uselist=False, 
        back_populates="restaurant",
        cascade="all, delete-orphan"
        )
    reviews = relationship("Review", back_populates="restaurant")
    categories = relationship(
        "Category", 
        secondary=restaurant_categories,
        back_populates="restaurants"
    )
    @validates('rating')
    def validate_rating(self, key, rating):
        if rating is not None and (rating < 0 or rating > 5):
            raise ValueError("Rating must be between 0 and 5")
        return rating
    @validates('price_level')
    def validate_price_level(self, key, price_level):
        if price_level is not None and not (0 <= price_level <= 4):
            raise ValueError("Price level must be between 0 and 4")
        return price_level


class Location(Base):
    __tablename__ = 'locations'
    
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    restaurant = relationship("Restaurant", back_populates="location")
    @validates('latitude')
    def validate_latitude(self, key, latitude):
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return latitude
        
    @validates('longitude')
    def validate_longitude(self, key, longitude):
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return longitude

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    author = Column(String)
    rating = Column(Float)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    sentiment_score = Column(Float)  # Для AI-анализа
    
    restaurant = relationship("Restaurant", back_populates="reviews")

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    restaurants = relationship(
        "Restaurant", 
        secondary=restaurant_categories,
        back_populates="categories"
    )