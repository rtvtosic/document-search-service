"""Заполнение БД данными из файла"""

from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import Session
from models import Base, Document

from config import sync_db_engine
from csv_parser import parse_data

# путь к csv-файлу относительно корня проекта, независимо от рабочего каталога
CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "posts.csv"

def fill_database():
    """Заполнение БД данными из файла"""
    # создание таблиц в базе данных
    Base.metadata.create_all(bind=sync_db_engine)

    # загрузка данных из csv-файла в правильном формате
    data = parse_data(path=str(CSV_PATH))

    # создание сессии и загрузка данных в БД
    try:
        with Session(bind=sync_db_engine) as db:
            # удаление данных перед загрузкой
            db.execute(text("TRUNCATE TABLE document RESTART IDENTITY"))
            db.commit()

            for obj in data:
                db.add(
                    Document(text=obj[0],
                            created_date=obj[1],
                            rubrics=obj[2])
                    )
            db.commit() # сохранение изменений в БД
        print("База данных успешно заполнена")
    except Exception as e:
        print(f"Возникла ошибка: {e}")


if __name__ == "__main__":
    fill_database()
