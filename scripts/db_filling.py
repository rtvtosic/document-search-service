from sqlalchemy import text
from sqlalchemy.orm import Session
from models import Base, Document

from scripts.csv_parser import parse_data
from config import db_engine


def fill_database():
    # создание таблиц в базе данных
    Base.metadata.create_all(bind=db_engine)

    # загрузка данных из csv-файла в правильном формате
    data = parse_data(path='posts.csv')

    # создание сессии и загрузка данных в БД
    try:
        with Session(bind=db_engine) as db:
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

