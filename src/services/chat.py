from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)

from src.keyboards.inline import InlineKeyboard
from src.utils.load_lexicon import LoaderLexicon
from src.utils.uow import UOW
from src.states import ChatStates


class ChatService:
    def __init__(self, language: str = "ru") -> None:
        self.language = language
        self.texts = LoaderLexicon(language=self.language).load_messages()
        self.uow = UOW()

    async def my_chats(
        self,
        callback: CallbackQuery,
    ) -> None:
        await callback.message.edit_text(
            text=self.texts["my_chats"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=[
                    "create_chat",
                    "find_message",
                    "export_dialog",
                    "your_chats",
                    "back",
                ],
                callback_datas=[
                    "create_chat",
                    "find_message",
                    "export_dialog",
                    "your_chats",
                    "menu",
                ],
            ),
        )

    async def send_message_create_chat(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        await state.set_state(ChatStates.waiting_for_chat_name)
        await callback.message.edit_text(text=self.texts["message_create_chat"])

    async def get_chat_name(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        async with self.uow:
            chat = await self.uow.chats.insert()

    async def create_chat(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None: ...
