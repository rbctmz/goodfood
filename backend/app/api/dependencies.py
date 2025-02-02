from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import SessionLocal

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()