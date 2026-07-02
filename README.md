# Сервис по поиску документов
Сервис полнотекстового поиска по документам, документы хранятся в PostgreSQL, поисковый индекс - в Elasticsearch

# Стек технологий
Python 3.12, SQLAlchemy, FastAPI, PostgreSQL, Elasticsearch, Docker

# Требования
* Python 3.12
* Docker
* Elasticsearch

## Установка
1. Клонируйте репозиторий:
```bash
git clone https://github.com/rtvtosic/test_task.git
cd test_task
```
2. Создайте и активируйте вирутальное окружение
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
# Postgres
docker run -d --name search-postgres -e POSTGRES_USER=search_user -e POSTGRES_PASSWORD=search_pass -e POSTGRES_DB=search_db -p 5432:5432 -v search_pgdata:/var/lib/postgresql/data postgres:16

# Elasticsearch
docker run -d --name search-elasticsearch -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" -p 9200:9200 elasticsearch:9.4.1
```

5. Заполните .env-файл данными, которые использовались при создании docker-контейнеров:
```
DB_USER=search_user
DB_PASSWORD=search_pass
DB_NAME=search_db
DB_HOST=localhost
DB_PORT=5432

ELASTIC_HOST=localhost
ELASTIC_PORT=9200
```


## Использование

### Подготовка данных (Создание БД, индекса и заполнение их данными)
```bash
cd scripts/
python load_data.py
```

### Запуск проекта
Для запуска сервиса используйте команду:
```bash
python main.py
```

## Структура проекта
- `main.py`

## Лицензия
Этот проект распространяется под лицензией MIT.