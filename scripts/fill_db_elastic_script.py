from scripts.db_filling import fill_database
from scripts.elastic_filling import fill_elastic


def fill_db_elastic():
    fill_database()
    fill_elastic()


if __name__ == "__main__":
    fill_db_elastic()