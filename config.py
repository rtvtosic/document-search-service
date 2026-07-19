"""Файл подключения к движку Postgres и клиенту Elastic"""

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from elasticsearch import AsyncElasticsearch, Elasticsearch
from dotenv import load_dotenv


# ==== Подключение к Postgres и ElasticSearch ====
load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

elastic_host = os.getenv("ELASTIC_HOST")
elastic_port = os.getenv("ELASTIC_PORT")

# асинхронные движки
async_db_engine = create_async_engine(f"postgresql+psycopg://{user}:{password}@{host}/{database}")
async_client = AsyncElasticsearch(
    hosts=[f"http://{elastic_host}:{elastic_port}"]
)

# синхронные движки
sync_db_engine = create_engine(f"postgresql+psycopg://{user}:{password}@{host}/{database}")
sync_client = Elasticsearch(
    hosts=[f"http://{elastic_host}:{elastic_port}"]
)