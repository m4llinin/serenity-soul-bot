from aiogram import (
    Router,
    F,
)
from aiogram.fsm.context import FSMContext

from aiogram.types import (
    Message,
    CallbackQuery,
)

from src.services.chat import ChatService

router = Router()


@router.callback_query(F.data == "create_chat")
async def create_chat(callback: CallbackQuery, state: FSMContext, language: str):
    await ChatService(language=language).send_message_create_chat(callback, state)
