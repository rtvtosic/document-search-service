"""Парсинг данных из .csv-файла"""

import ast
from datetime import datetime
import pandas as pd


def parse_data(path: str) -> list:
    """Парсинг данных из .csv-файла"""
    data = pd.read_csv(path)
    formatted_data = []

    for row in data.itertuples():
        text = row.text
        created_date = row.created_date
        rubrics = row.rubrics

        formatted_created_date = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S")
        formatted_rubrics = ast.literal_eval(rubrics)

        formatted_data.append((text, formatted_created_date, formatted_rubrics))

    return formatted_data


if __name__ == "__main__":
    parse_data('posts.csv')
