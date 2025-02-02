from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes.reviews import router as reviews_router
from .api.routes.cafes import router as cafes_router
from .db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Действия при запуске и остановке приложения"""
    # Инициализация при запуске
    init_db()
    yield
    # Очистка при остановке
    pass

app = FastAPI(
    title="GoodFood API",
    description="API для поиска и анализа ресторанов",
    version="1.0.0",
    lifespan=lifespan
)

# Подключаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(reviews_router, prefix="/restaurants")
# Подключаем роутеры без префикса, так как он уже указан в роутерах
# app.include_router(reviews_router)
app.include_router(cafes_router)