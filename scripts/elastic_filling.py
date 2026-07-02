from elasticsearch.helpers import bulk
from sqlalchemy.orm import Session
from models import Document

from config import client, db_engine


# ==== Выгрузка данных из БД в индекс ====
# создание сессии и загрузка данных в БД

def fill_elastic():
    # удаление индекса если есть
    if client.indices.exists(index="documents"):
        client.indices.delete(index="documents")

    # создание нового индекса
    mappings = {
        "properties": {
            "id": {"type": "integer"},
            "text": {"type": "text"}
        }
    }

    client.indices.create(index="documents", mappings=mappings)

    try:
        with Session(bind=db_engine) as db:
            documents = db.query(Document).all()
            total = len(documents)
            documents_dict = [{"_index": "documents", "_id": doc.id, "_source": {"id": doc.id, "text": doc.text}} for doc in documents]
            
            success, failed = bulk(client, documents_dict)
            print(f"Успешно: {success}, Failed: {len(failed)}, Всего: {total}")
                
    except Exception as e:
        print(f"Возникла ошибка: {e}")


if __name__ == "__main__":
    fill_elastic()
