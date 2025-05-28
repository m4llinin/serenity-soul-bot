from aiogram import (
    Router,
    F,
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from aiogram.types import (
    Message,
    CallbackQuery,
)

from src.services.menu import MenuService
from src.services.profile import ProfileService
from src.services.settings import SettingsService
from src.services.chat import ChatService
from src.utils.load_lexicon import LoaderLexicon

router = Router()

buttons = LoaderLexicon("ru").load_keyboard()


@router.message(F.text == buttons["my_profile"])
async def my_profile(message: Message, state: FSMContext, language: str):
    await ProfileService(language).profile(message, state)


@router.message(F.text == buttons["settings"])
async def settings(message: Message, state: FSMContext, language: str):
    await SettingsService(language).settings_menu(message, state)


@router.message(F.text == buttons["my_chats"])
async def chat(message: Message, state: FSMContext, language: str):
    await ChatService(language).my_chats(message, state)
