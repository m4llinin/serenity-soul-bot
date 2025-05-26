from sqlalchemy.orm import (
    mapped_column,
    Mapped,
)

from src.core.database.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str]
    price: Mapped[float]
    limit_queries: Mapped[int] = mapped_column(nullable=True)
