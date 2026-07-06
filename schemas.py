"""Pydantic-схемы"""

from datetime import datetime
from pydantic import BaseModel


class SearchRequest(BaseModel):
    """Схема для отправки запроса"""
    query: str


class DocumentSchema(BaseModel):
    """Схема обьекта Document"""
    id: int
    text: str
    created_date: datetime
    rubrics: list[str]

    # разрешает собирать pydantic-схему прямо из ORM-объекта
    model_config = {"from_attributes": True}
