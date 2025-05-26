from datetime import (
    datetime,
    UTC,
)

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
)

from src.utils.load_lexicon import LoaderLexicon
from src.keyboards.inline import InlineKeyboard
from src.utils.uow import UOW
from src.states import SupportStates
from src.core.config import TelegramConfig


class SupportService:
    def __init__(self, language: str = "ru") -> None:
        self.language = language
        self.texts = LoaderLexicon(language=self.language).load_messages()
        self.uow = UOW()

    async def send_improvement_message(self, callback: CallbackQuery) -> None:
        await callback.message.edit_text(
            text=self.texts["improvement"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=["write", "back"],
                callback_datas=["write_improvement", "my_profile"],
            ),
        )

    async def write_improvement(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        async with self.uow:
            user = await self.uow.users.get_one({"id": callback.message.chat.id})
            if (
                user.last_support_message
                and (
                    datetime.now(tz=UTC).timestamp()
                    - user.last_support_message.timestamp()
                )
                < 60 * 60 * 24
            ):
                await callback.answer(
                    text=self.texts["error_not_time_improvement"],
                    show_alert=True,
                )
                return

            await state.set_state(SupportStates.get_improvement_message)
            await callback.message.edit_reply_markup(
                reply_markup=InlineKeyboard(self.language).keyboard_column(
                    keys=["writing"],
                    callback_datas=["None"],
                )
            )

    async def get_improvement_message(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        await message.bot.send_message(
            chat_id=TelegramConfig.ADMIN_CHAT,
            text=self.texts["new_improvement"],
        )
        await message.forward(chat_id=TelegramConfig.ADMIN_CHAT)

        async with self.uow:
            await self.uow.users.update(
                filters={"id": message.chat.id},
                data={"last_support_message": datetime.now(tz=UTC)},
            )
            await self.uow.commit()

        await state.set_state(None)
        await message.answer(
            self.texts["get_improvement_message"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=["ready"], callback_datas=["improvement"]
            ),
        )

    async def support(self, callback: CallbackQuery) -> None:
        await callback.message.edit_text(
            text=self.texts["support"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=["write", "back"],
                callback_datas=["write_support", "my_profile"],
            ),
        )

    async def write_support(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        await state.set_state(SupportStates.get_support_message)
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=["writing"],
                callback_datas=["None"],
            )
        )

    async def get_support_message(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        await message.forward(chat_id=TelegramConfig.ADMIN_CHAT)
        await message.bot.send_message(
            chat_id=TelegramConfig.ADMIN_CHAT,
            text=self.texts["new_support"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=["reply"],
                callback_datas=[f"reply_support_{message.chat.id}"],
            ),
        )

        await state.set_state(None)
        await message.answer(
            self.texts["get_support_message"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=["ready"], callback_datas=["support"]
            ),
        )

    async def write_support_reply(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        await state.update_data(user_id=callback.data.split("_")[2], msg=callback)
        await state.set_state(SupportStates.get_support_reply)
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=["writing"],
                callback_datas=["None"],
            )
        )

    async def get_support_reply(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        user_id = await state.get_value("user_id")
        callback = await state.get_value("msg")

        await message.bot.send_message(
            chat_id=user_id,
            text=self.texts["support_reply"].format(reply=message.text),
        )

        await state.set_state(None)
        await callback.message.edit_reply_markup(
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=["ready"],
                callback_datas=["None"],
            )
        )
