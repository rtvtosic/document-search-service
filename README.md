# Сервис по поиску документов
Сервис полнотекстового поиска по документам, документы хранятся в PostgreSQL, поисковый индекс - в Elasticsearch. Сервис обернут в Docker, а также весь функционал покрыт тестами

## Стек технологий
Python 3.12, SQLAlchemy, FastAPI, PostgreSQL, Elasticsearch, Docker

## Требования
* Python 3.12 (для локального запуска)
* Docker (для обоих вариантов)
* Docker Compose (для запуска через Docker Compose)

## Подготовка репозитория
Клонируйте репозиторий:
```bash
git clone https://github.com/rtvtosic/test_task.git
cd test_task
```

Создайте `.env`-файл (скопируйте `.env.example`) и укажите пароль:
```
DB_USER=search_user
DB_PASSWORD=your_password   # укажите свой пароль
DB_NAME=search_db
DB_HOST=localhost
DB_PORT=5432

ELASTIC_HOST=localhost
ELASTIC_PORT=9200
```

Ниже описаны два варианта запуска: [через Docker Compose](#вариант-1-запуск-через-docker-compose-рекомендуется) (рекомендуется) и [локально](#вариант-2-локальный-запуск).


## Вариант 1. Запуск через Docker Compose (рекомендуется)
Поднимает сразу три сервиса: приложение (`app`), PostgreSQL и Elasticsearch.

> В этом варианте значения `DB_HOST` и `ELASTIC_HOST` из `.env` автоматически
> переопределяются на имена сервисов (`postgres` и `elasticsearch`) — менять их вручную не нужно.

1. Соберите и запустите все сервисы:
```bash
docker compose up -d --build
```
Приложение дождётся готовности БД и Elasticsearch (настроены healthcheck).

2. Проверьте, что контейнеры поднялись:
```bash
docker compose ps
```

3. Загрузите данные (создание таблиц, индекса и наполнение) — **внутри контейнера app**:
```bash
docker compose exec app python scripts/load_data.py
```

4. Сервис доступен на `http://localhost:8000`, документация — `http://localhost:8000/docs`.

### Управление контейнерами
```bash
docker compose logs -f app      # логи приложения
docker compose stop             # остановить
docker compose up -d            # запустить снова
docker compose down             # остановить и удалить контейнеры
docker compose down -v          # то же + удалить данные (том search_pgdata)
```


## Вариант 2. Локальный запуск
Приложение запускается на хосте, а PostgreSQL и Elasticsearch — в отдельных docker-контейнерах.

1. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv # создание окружения
```
Активация на Linux/MacOS:
```bash
source venv/bin/activate
```
Активация на Windows (PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

2. Установите необходимые библиотеки:
```bash
pip install -r requirements.txt
```

3. Создайте и запустите docker-контейнеры с БД и индексом:
```bash
# Postgres (пароль должен совпадать с DB_PASSWORD из .env)
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

4. Убедитесь, что в `.env` указаны `DB_HOST=localhost` и `ELASTIC_HOST=localhost`.

5. Загрузите данные (создание базы данных, индекса и заполнение их данными):
```bash
cd scripts/
python load_data.py
cd ..
```

6. Запустите проект:
```bash
python main.py
```
Сервис поднимется на адресе `http://localhost:8000`, **интерактивная документация** — `http://localhost:8000/docs`.


## Запуск тестов
Тесты обращаются к реальным `PostgreSQL` и `Elasticsearch`,
поэтому перед запуском нужно, чтобы сервисы были подняты и данные загружены
(шаги из любого из вариантов запуска выше, включая `load_data.py`).

### Вариант 1. Локально
Убедитесь, что контейнеры с БД и Elasticsearch запущены, данные загружены,
а виртуальное окружение активировано. Затем из корня проекта выполните команду:
```bash
pytest -v
```

### Вариант 2. Внутри контейнера app (Docker Compose)
```bash
docker compose exec app pytest -v
```

Тесты покрывают:
- поиск документов по тексту (`POST /search`);
- ограничение выдачи (не более 20 результатов);
- удаление существующего документа из БД и индекса (`DELETE /documents/{id}`);
- корректный ответ `404` при удалении несуществующего документа.


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
- `Dockerfile` - Образ приложения.
- `docker-compose.yml` - Оркестрация app + PostgreSQL + Elasticsearch.
- `tests/test_main.py` - Тесты, покрывающие функционал сервиса.

## Лицензия
Этот проект распространяется под лицензией MIT.
