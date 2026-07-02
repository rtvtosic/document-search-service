import sys
from pathlib import Path

# корень проекта в sys.path, чтобы были видны модули config и models из корня репозитория
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from db_filling import fill_database
from elastic_filling import fill_elastic


def fill_db_elastic():
    fill_database()
    fill_elastic()


if __name__ == "__main__":
    fill_db_elastic()