import logging
import os
from parser.core.config import settings

import pandas


def parse_xls_bulletin_to_dict(date: str) -> list[dict[str, str | float]] | None:
    """Parses .xls file for bulletin data into a list of dictonaries.

    Args:
        date (str): Date of daily bulletin using to found .xls file

    Returns:
        list[dict[str, str | float]] | None: List of dictionaries representing parsed data,
        or 'None' if the file doesn't exist or contains invalid data
    """

    file_path = os.path.join(settings.DOWNLOAD_DIR, f"{date}.xls")

    if not os.path.exists(file_path):
        logging.error(msg=f"File {file_path} doens't exist")
        return None

    start_row = None
    table_start = "Единица измерения: Метрическая тонна"
    df = pandas.read_excel(file_path, header=None)
    for idx, row in df.iterrows():
        if table_start in row.astype(str).tolist():
            start_row = idx + 1
            break

    if start_row is None:
        logging.error(msg=f"Invalid data in file {file_path}")
        return None

    df = pandas.read_excel(file_path, skiprows=start_row, usecols="B:F,O", skipfooter=2)
    df.columns = df.columns.str.replace("\n", " ", regex=True)

    to_numeric_columns = [
        "Количество Договоров, шт.",
        "Обьем Договоров, руб.",
        "Объем Договоров в единицах измерения",
    ]

    for column in to_numeric_columns:
        df[column] = pandas.to_numeric(df[column], errors="coerce")

    df_filtered = df[df["Количество Договоров, шт."] > 0]

    df_filtered = df_filtered.rename(
        columns={
            "Код Инструмента": "exchange_product_id",
            "Наименование Инструмента": "exchange_product_name",
            "Базис поставки": "delivery_basis_name",
            "Объем Договоров в единицах измерения": "volume",
            "Обьем Договоров, руб.": "total",
            "Количество Договоров, шт.": "count",
        }
    )[
        [
            "exchange_product_id",
            "exchange_product_name",
            "delivery_basis_name",
            "volume",
            "total",
            "count",
        ]
    ].dropna()

    result = df_filtered.to_dict(orient="records")
    for item in result:
        item["date"] = date

    return result
