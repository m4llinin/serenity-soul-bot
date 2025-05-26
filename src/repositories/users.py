from sqlalchemy import text

from src.core.database.base import SqlAlchemyRepository
from src.models.user import User


class UsersRepository(SqlAlchemyRepository):
    _model = User

    async def get_count_partners_and_subscriptions(
        self,
        user_id: int,
    ) -> dict[str, int | None]:
        stmt = text(
            """SELECT COUNT(*) as count_partners, 
        COUNT(*) FILTER (WHERE subscription <> 1) as count_subscriptions 
        FROM users
        WHERE partner_id=:user_id;"""
        )
        res = await self._session.execute(stmt, {"user_id": user_id})
        return [dict(row) for row in res.mappings()][0]
