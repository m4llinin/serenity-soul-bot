from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
)

from src.utils.load_lexicon import LoaderLexicon
from src.keyboards.inline import InlineKeyboard
from src.utils.uow import UOW
from src.utils.ai_client import DeepseekClient


class ProfileService:
    def __init__(self, language: str = "ru") -> None:
        self.language = language
        self.texts = LoaderLexicon(language=self.language).load_messages()
        self.uow = UOW()

    async def profile(self, callback: CallbackQuery) -> None:
        async with self.uow:
            await callback.message.edit_text(text=self.texts["loading"])

            user = await self.uow.users.get_one({"id": callback.message.chat.id})
            if not user:
                await callback.message.edit_text(
                    text=self.texts["error_not_found_user"]
                )

            subscription = await self.uow.subscriptions.get_one(
                {"id": user.subscription}
            )
            date_end_subscription = (
                user.date_end_subscription.strftime("%d.%m.%Y")
                if user.date_end_subscription
                else "∞"
            )

            prompts = LoaderLexicon(self.language).load_prompts()
            client = DeepseekClient()
            await callback.message.edit_text(
                text=self.texts["my_profile"].format(
                    id=user.id,
                    subscription=subscription.name,
                    date_end=date_end_subscription,
                    level_happiness=5,
                    current_queries=user.queries,
                    limit_queries=subscription.limit_queries,
                    phrase=await client.get_phrase_of_the_day(
                        user_id=user.id,
                        prompt=prompts["user_phrase_day"],
                        system_message=prompts["system_phrase_day"],
                    ),
                ),
                reply_markup=InlineKeyboard(self.language).keyboard_column(
                    keys=[
                        "my_condition",
                        "progress_diary",
                        "settings",
                        "partners",
                        "subscription",
                        "support",
                        "improvement",
                        "back",
                    ],
                    callback_datas=[
                        "my_condition",
                        "progress_diary",
                        "settings",
                        "partners",
                        "buy_subscription",
                        "support",
                        "improvement",
                        "menu",
                    ],
                ),
            )

    async def partner(self, callback: CallbackQuery) -> None:
        async with self.uow:
            statistics = await self.uow.users.get_count_partners_and_subscriptions(
                callback.message.chat.id
            )

            await callback.message.edit_text(
                text=self.texts["partner"].format(
                    count_partners=statistics["count_partners"],
                    count_subscriptions=statistics["count_subscriptions"],
                ),
                reply_markup=InlineKeyboard(self.language).partner(
                    callback.message.chat.id
                ),
            )
