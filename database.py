"""Модуль для создания движка PostgreSQL"""

from sqlalchemy.orm import Session
from config import sync_db_engine


def get_db():
    """Создание движка для подключения к PostgreSQL"""
    db = Session(bind=sync_db_engine)
    try:
        yield db
    finally:
        db.close()
