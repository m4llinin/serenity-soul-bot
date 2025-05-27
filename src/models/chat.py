from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.core.database.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    chat_name: Mapped[str] = mapped_column(nullable=False)

    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)

    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
