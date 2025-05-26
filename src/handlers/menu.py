from aiogram import (
    Router,
    F,
)
from aiogram.filters import Command

from aiogram.types import (
    Message,
    CallbackQuery,
)

from src.services.menu import MenuService
from src.services.profile import ProfileService
from src.services.settings import SettingsService

router = Router()


@router.message(Command("menu"))
async def menu(message: Message, language: str):
    await MenuService(language).main_menu(message)


@router.callback_query(F.data == "menu")
async def menu(callback: CallbackQuery, language: str):
    await MenuService(language).main_menu_from_callback(callback)


@router.callback_query(F.data == "my_profile")
async def my_profile(callback: CallbackQuery, language: str):
    await ProfileService(language).profile(callback)


@router.callback_query(F.data == "settings")
async def settings(callback: CallbackQuery, language: str):
    await SettingsService(language).settings_menu(callback)
