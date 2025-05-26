import asyncio
import random
from datetime import datetime

from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
)

from src.utils.load_lexicon import LoaderLexicon
from src.keyboards.inline import InlineKeyboard
from src.utils.uow import UOW
from src.utils.ai_client import DeepseekClient
from src.utils.auido_converter import AudioConverter


class MenuService:
    def __init__(self, language: str = "ru") -> None:
        self.language = language
        self.texts = LoaderLexicon(language=self.language).load_messages()
        self.uow = UOW()

    async def main_menu(self, message: Message) -> None:
        await message.answer(
            text=self.texts["main_menu"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=[
                    "my_profile",
                    "settings",
                    "analyze",
                    "my_chats",
                    "biblioteca",
                    "subscription",
                ],
                callback_datas=[
                    "my_profile",
                    "settings",
                    "analyze",
                    "my_chats",
                    "biblioteca",
                    "subscription",
                ],
            ),
        )

    async def main_menu_from_callback(self, callback: CallbackQuery) -> None:
        await callback.message.edit_text(
            text=self.texts["main_menu"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=[
                    "my_profile",
                    "settings",
                    "analyze",
                    "my_chats",
                    "biblioteca",
                    "subscription",
                ],
                callback_datas=[
                    "my_profile",
                    "settings",
                    "analyze",
                    "my_chats",
                    "biblioteca",
                    "subscription",
                ],
            ),
        )