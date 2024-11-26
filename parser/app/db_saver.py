import datetime
from parser.core.database import AsyncSessionFactory
from parser.models import SpimexTradingResult


async def save_bulletin_to_db(data: list[dict[str, str | float]]) -> None:
    """Save bulletin data to database.

    Args:
        data (list[dict[str, str  |  float]]): List of dictionaries, representing
        trades in bulletin
    """

    models = []
    for record_data in data:
        data_to_sql = {
            "exchange_product_id": record_data.get("exchange_product_id"),
            "exchange_product_name": record_data.get("exchange_product_name"),
            "oil_id": record_data.get("exchange_product_id")[:4],
            "delivery_basis_id": record_data.get("exchange_product_id")[4:7],
            "delivery_basis_name": record_data.get("delivery_basis_name"),
            "delivery_type_id": record_data.get("exchange_product_id")[-1],
            "volume": int(record_data.get("volume")),
            "total": int(record_data.get("total")),
            "count": int(record_data.get("count")),
            "date": datetime.datetime.strptime(record_data.get("date"), "%d.%m.%Y"),
        }
        models.append(SpimexTradingResult(**data_to_sql))

        async with AsyncSessionFactory() as session:
            session.add_all(models)
            await session.commit()
