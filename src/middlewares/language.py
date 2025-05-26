from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.types import TelegramObject

from src.utils.uow import UOW


class LanguageMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.uow = UOW()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if "event_context" in data and isinstance(data["event_context"], EventContext):
            user_id = data["event_context"].chat.id

            async with self.uow:
                user = await self.uow.users.get_one({"id": user_id})

                if not user:
                    data["language"] = "ru"
                else:
                    data["language"] = user.language

        return await handler(event, data)
