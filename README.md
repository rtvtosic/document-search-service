# Сервис по поиску документов
Сервис полнотекстового поиска по документам, документы хранятся в PostgreSQL, поисковый индекс — в Elasticsearch

# Стек технологий
Python 3.12, SQLAlchemy, FastAPI, PostgreSQL, Elasticsearch, Docker

# Требования
* Python 3.12
* Docker

## Установка
1. Клонируйте репозиторий:
```bash
git clone https://github.com/rtvtosic/test_task.git
cd test_task
```
2. Создайте и активируйте виртуальное окружение
```bash
python -m venv venv # создание окружения
```
Активация на Linux/MacOS:
```bash
source venv/bin/activate
```
Активация на Windows:
```bash
venv/Scripts/Activate.ps1
```
3. Установите необходимые библиотеки:
```bash
pip install -r requirements.txt
```

4. Создайте и запустите docker-контейнеры:
```bash
# Postgres (укажите свой пароль вместо your_password)
docker run -d --name search-postgres -e POSTGRES_USER=search_user -e POSTGRES_PASSWORD=your_password -e POSTGRES_DB=search_db -p 5432:5432 -v search_pgdata:/var/lib/postgresql/data postgres:16

# Elasticsearch
docker run -d --name search-elasticsearch -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" -p 9200:9200 elasticsearch:9.4.1

# проверьте, что контейнеры поднялись (в списке должны быть search-postgres и search-elasticsearch со статусом Up)
docker ps
```
Остановка контейнеров:
```bash
docker stop search-postgres search-elasticsearch
```
Повторный запуск контейнеров:
```bash
docker start search-postgres search-elasticsearch
```

5. Заполните .env-файл данными (скопируйте `.env.example`-файл), которые использовались при создании docker-контейнеров:
```
DB_USER=search_user
DB_PASSWORD=... # ваш пароль
DB_NAME=search_db
DB_HOST=localhost
DB_PORT=5432

ELASTIC_HOST=localhost
ELASTIC_PORT=9200
```

## Использование
### Подготовка данных (Создание базы данных, индекса и заполнение их данными)
```bash
cd scripts/
python load_data.py
```

### Запуск проекта
После подготовки данных используйте команду для запуска:
```bash
python main.py
```
Сервис поднимется на адресе `http://localhost:8000`

## Описание эндпоинтов
* `POST /search` — тело `{"query": "текст"}`, возвращает список документов (id, text, created_date, rubrics), первые 20, по убыванию created_date.
* `DELETE /documents/{doc_id}` — удаление из БД и индекса.

Интерактивная документация с возможностью тестирования эндпоинтов находится на адресе `http://localhost:8000/docs`

## Структура проекта
- `main.py` - Главный файл проекта
- `config.py` - Подключение к движку Postgres и клиенту Elasticsearch.
- `database.py` - Создание сессии для работы с SQLAlchemy.
- `docs.json` - Документация API в формате OpenAPI.
- `models.py` - Модели данных для БД.
- `schemas.py` - Pydantic-схемы для эндпоинтов.
- `scripts/` - Скрипты для подготовки данных и загрузки их в БД и индекс.
- `data/posts.csv` - Исходные данные для БД.
- `requirements.txt` - Список зависимостей.
- `.env.example` - Шаблон файла окружения.

## Лицензия
Этот проект распространяется под лицензией MIT.