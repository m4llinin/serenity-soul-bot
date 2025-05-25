from sqlalchemy import select

from src.core.database.base import SqlAlchemyRepository
from src.models.user import User


class UsersRepository(SqlAlchemyRepository):
    _model = User
