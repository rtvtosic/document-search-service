import sys
import pytest
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session

# корень проекта в sys.path, чтобы были видны модули config и models из корня репозитория
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from config import db_engine, client as es_client
from models import Document
from main import app


client = TestClient(app)

def test_search_returns_ok():
    response = client.post("/search", json={"query": "информация"})
    assert response.status_code == 200


def test_length_le_than_20():
    response = client.post("/search", json={"query": "информация"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 20


def test_delete_nonexistent():
    responce = client.delete("/documents/9999999")
    assert responce.status_code == 404


@pytest.fixture
def temp_document():
    with Session(bind=db_engine) as db:
        doc = Document(
            text="временный тестовый документ для проверки удаления",
            created_date=datetime.now(),
            rubrics=["TEST"]
        )
        db.add(doc)
        db.commit()
        doc_id = doc.id
        doc_text = doc.text
    
    es_client.index(
        index="documents",
        id=doc_id,
        document={"id": doc_id, "text": doc_text}
    )

    yield doc_id

    with Session(bind=db_engine) as db:
        leftover = db.get(Document, doc_id)
        if leftover is not None:
            db.delete(leftover)
            db.commit()
    try:
        es_client.delete(index="documents", id=str(doc_id))
    except Exception:
        pass


def test_delete_existing_document(temp_document):
    doc_id = temp_document

    response = client.delete(f"/documents/{doc_id}")
    assert response.status_code == 200 

    # проверка что документ удален из БД
    with Session(bind=db_engine) as db:
        assert db.get(Document, doc_id) is None

    # проверка что документ удален из индекса ES
    assert not es_client.exists(index="documents", 
                            id=str(doc_id))
