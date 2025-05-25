from src.repositories.users import UsersRepository
from src.repositories.subscriptions import SubscriptionsRepository

from src.core.utils.uow import UnitOfWork


class UOW(UnitOfWork):
    async def __aenter__(self):
        await super().__aenter__()

        self.users = UsersRepository(self.session)
        self.subscriptions = SubscriptionsRepository(self.session)
