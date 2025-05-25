from src.core.database.base import SqlAlchemyRepository
from src.models.subscription import Subscription


class SubscriptionsRepository(SqlAlchemyRepository):
    _model = Subscription
