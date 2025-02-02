import pytest
from backend.app.db.session import get_db # или нужный модуль, где определена get_db
from sqlalchemy.orm import Session

@pytest.mark.asyncio
async def test_get_db_returns_session():
    # Получаем асинхронный генератор
    db_gen = get_db()
    # Получаем первую выдачу из асинхронного генератора
    db = await db_gen.__anext__()
    # Проверяем, что объект является экземпляром Session
    assert isinstance(db, Session)
    # Завершаем генератор и проверяем, что он больше не выдаёт значений
    with pytest.raises(StopAsyncIteration):
        await db_gen.__anext__()