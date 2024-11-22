import datetime

from parser.core.database import engine
from parser.models.base_model import Base
from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column


class SpimexTradingResult(Base):
    __tablename__ = "spimex_trading_results"

    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[int]
    total: Mapped[int]
    count: Mapped[int]
    date: Mapped[datetime.date] = mapped_column(Date)
