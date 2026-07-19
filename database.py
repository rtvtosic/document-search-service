"""Модуль выдачи асинхронной сессии БД как зависимости FastAPI"""

from sqlalchemy.ext.asyncio import async_sessionmaker
from config import async_db_engine

AsyncSessionLocal = async_sessionmaker(
    bind=async_db_engine,
    expire_on_commit=False
)

async def get_db():
    """Создание движка для подключения к PostgreSQL"""

    async with AsyncSessionLocal() as db:
        yield db
    
