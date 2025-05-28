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
from src.states import ChatStates

router = Router()


@router.callback_query(F.data == "create_chat")
async def create_chat(callback: CallbackQuery, state: FSMContext, language: str):
    await ChatService(language=language).send_message_create_chat(callback, state)


@router.message(F.text, ChatStates.waiting_for_chat_name)
async def get_chat_name(message: Message, state: FSMContext, language: str):
    await ChatService(language=language).get_chat_name(message, state)


@router.callback_query(F.data == "your_chats")
async def your_chats(callback: CallbackQuery, state: FSMContext, language: str):
    await ChatService(language=language).choose_current_chat(callback, state)


@router.callback_query(lambda x: x.data.startswith("choose_chat_"))
async def your_chats(callback: CallbackQuery, state: FSMContext, language: str):
    await ChatService(language=language).set_current_chat(callback, state)


@router.callback_query(F.data == "export_dialog")
async def export_dialog(callback: CallbackQuery, state: FSMContext, language: str):
    await ChatService(language=language).export_chat_to_pdf(callback, state)
