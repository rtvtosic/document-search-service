"""Модели данных для БД"""

from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Text, DateTime
from sqlalchemy.dialects.postgresql import ARRAY


class Base(DeclarativeBase):
    """Базовый класс"""


class Document(Base):
    """Модель документа"""
    __tablename__ = "document"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime)
    rubrics: Mapped[list[str]] = mapped_column(ARRAY(String))
