from datetime import datetime
from enum import Enum

from sqlalchemy import (
    func,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.core.database.base import Base


class CommunicationStyles(str, Enum):
    FRIEND = "friend"
    TEACHER = "teacher"
    NEUTRAL = "neutral"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    partner_id: Mapped[int] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(default="", nullable=True)
    communication_style: Mapped[CommunicationStyles] = mapped_column(
        default=CommunicationStyles.NEUTRAL.value,
        nullable=False,
    )
    is_first_start: Mapped[bool] = mapped_column(default=True, nullable=False)
    last_activity: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    subscription: Mapped[int] = mapped_column(
        ForeignKey("subscriptions.id"),
        default=1,
        nullable=False,
    )
    date_end_subscription: Mapped[datetime] = mapped_column(nullable=True)
    queries: Mapped[int] = mapped_column(default=20, nullable=False)
    last_support_message: Mapped[datetime] = mapped_column(nullable=True)
    language: Mapped[str] = mapped_column(default="ru", nullable=True)
