from aiogram import (
    Router,
    F,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
)

from src.states import SupportStates
from src.services.profile import ProfileService
from src.services.support import SupportService

router = Router()


@router.callback_query(F.data == "partners")
async def settings(callback: CallbackQuery, language: str) -> None:
    await ProfileService(language).partner(callback)


@router.callback_query(F.data == "improvement")
async def improvement(callback: CallbackQuery, language: str) -> None:
    await SupportService(language).send_improvement_message(callback)


@router.callback_query(F.data == "write_improvement")
async def write_improvement(
    callback: CallbackQuery,
    state: FSMContext,
    language: str,
) -> None:
    await SupportService(language).write_improvement(callback, state)


@router.message(F.text | F.voice, SupportStates.get_improvement_message)
async def get_improvement(message: Message, state: FSMContext, language: str) -> None:
    await SupportService(language).get_improvement_message(message, state)


@router.callback_query(F.data == "support")
async def support(callback: CallbackQuery, language: str) -> None:
    await SupportService(language).support(callback)


@router.callback_query(F.data == "write_support")
async def write_support(
    callback: CallbackQuery,
    state: FSMContext,
    language: str,
) -> None:
    await SupportService(language).write_support(callback, state)


@router.message(F.text | F.voice, SupportStates.get_support_message)
async def get_support(message: Message, state: FSMContext, language: str) -> None:
    await SupportService(language).get_support_message(message, state)


@router.callback_query(lambda x: x.data.startswith("reply_support_"))
async def write_support_reply(
    callback: CallbackQuery,
    state: FSMContext,
    language: str,
) -> None:
    await SupportService(language).write_support_reply(callback, state)


@router.message(F.text, SupportStates.get_support_reply)
async def get_support_reply(message: Message, state: FSMContext, language: str) -> None:
    await SupportService(language).get_support_reply(message, state)
