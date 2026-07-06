"""Модуль для создания движка PostgreSQL"""

from sqlalchemy.orm import Session
from config import db_engine


def get_db():
    """Создание движка для подключения к PostgreSQL"""
    db = Session(bind=db_engine)
    try:
        yield db
    finally:
        db.close()
