from aiogram import (
    Router,
    F,
)
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
)

from src.services.start import StartService
from src.states import StartingStates

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await StartService().start_message(message)


@router.callback_query(lambda x: x.data in ("enter_name", "you", "neutral_name"))
async def send_question_2(callback: CallbackQuery, state: FSMContext):
    await StartService().get_answer_on_start_question_1(callback=callback, state=state)


@router.message(F.text, StartingStates.get_name)
async def get_user_name(message: Message, state: FSMContext):
    await StartService().get_user_name(message=message, state=state)


@router.callback_query(
    lambda x: x.data
    in ("calm_down", "sort_relationship", "inside_myself", "want_talk", "urgent")
)
async def send_question_3(callback: CallbackQuery, state: FSMContext):
    await StartService().get_answer_on_start_question_2(callback=callback, state=state)


@router.message(F.voice, StartingStates.get_urgent_voice)
async def get_urgent_voice(message: Message, state: FSMContext):
    await StartService().get_voice_message_urgent(message=message, state=state)


@router.message(F.text, StartingStates.get_urgent_voice)
async def get_urgent_voice(message: Message, state: FSMContext):
    await StartService().get_voice_message_urgent(message=message, state=state)


@router.callback_query(StartingStates.get_feelings)
async def send_question_4(callback: CallbackQuery, state: FSMContext):
    await StartService().get_answer_on_start_question_3(callback=callback, state=state)
