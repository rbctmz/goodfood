from .models import Base
from .session import engine

def init_db():
    Base.metadata.create_all(bind=engine)