from src.core.database.base import SqlAlchemyRepository
from src.models.chat import (
    Chat,
    Message,
)


class ChatsRepository(SqlAlchemyRepository):
    _model = Chat


class MessagesRepository(SqlAlchemyRepository):
    _model = Message
