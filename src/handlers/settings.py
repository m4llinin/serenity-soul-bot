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

from src.utils.load_lexicon import LoaderLexicon
from src.services.settings import SettingsService

router = Router()


@router.callback_query(F.data == "model")
async def settings(callback: CallbackQuery, language: str):
    await SettingsService(language).choose_model(callback)


@router.callback_query(
    lambda query: query.data in ("short", "pretty", "light", "strict")
)
async def settings(callback: CallbackQuery, language: str):
    await SettingsService(language).get_chosen_model(callback)


@router.callback_query(F.data == "communication_style")
async def communication_style(callback: CallbackQuery, language: str):
    await SettingsService(language).choose_communication_style(callback)


@router.callback_query(lambda query: query.data in ("friend", "teacher", "neutral"))
async def communication_style(callback: CallbackQuery, language: str):
    await SettingsService(language).get_chosen_communication_style(callback)


@router.callback_query(F.data == "language")
async def get_language(callback: CallbackQuery, language: str):
    await SettingsService(language).choose_language(callback)


@router.callback_query(lambda query: query.data in LoaderLexicon().get_languages)
async def get_language(callback: CallbackQuery, language: str):
    await SettingsService(language).get_chosen_language(callback)
