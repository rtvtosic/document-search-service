"""Главный файл проекта с реализацией эндпоинтов"""
import uvicorn

from elasticsearch import NotFoundError
from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy import desc
from sqlalchemy.orm import Session
from models import Document

from database import get_db
from config import client

from schemas import SearchRequest, DocumentSchema


app = FastAPI(
    title="Сервис поиска документов"
)

# поиск документа по тексту
@app.post("/search",
        response_model=list[DocumentSchema],
        tags=["Методы"],
        summary="Поиск документа по тексту")
def search_docs_by_text(request: SearchRequest,
                        db: Session = Depends(get_db)):
    """Поиск документа по тексту"""

    # ==== Поиск нужных id в индексе в Elasticsearch ====
    document_ids = []
    result_documents = []

    resp = client.search(
        index="documents",
        query={
            "match": {
                "text": request.query
            }
        },
        size=20
    )

    for doc in resp['hits']['hits']:
        document_ids.append(doc['_source']['id'])

    # ==== Поиск данных по id в Postgres ====
    query = db.query(Document).filter(
        Document.id.in_(document_ids)
    ).order_by(desc(Document.created_date)).all()

    for doc in query:
        result_documents.append(doc)

    return result_documents

# удалять документ из БД и индекса по полю id.
@app.delete("/documents/{doc_id}",
            tags=["Методы"],
            summary="Удаление документа из БД и индекса по id")
def delete_doc_by_id(doc_id: int, db: Session = Depends(get_db)):
    """Удаление документа из БД и индекса по полю id"""

    # удаление из Postgres
    doc_to_delete = db.get(Document, doc_id)

    if doc_to_delete is None:
        raise HTTPException(status_code=404, detail="Document Not Found")

    db.delete(doc_to_delete)
    db.commit()

    # удаление из Elasticsearch
    try:
        client.delete(index="documents", id=str(doc_id))
    except NotFoundError:
        pass

    return {"detail": "Document deleted"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
