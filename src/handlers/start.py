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
from src.states import StartingStates, ChatStates

router = Router()


@router.message(CommandStart())
async def start_and_send_question_1(message: Message, state: FSMContext, language: str):
    await StartService(language).start_message(message, state)


@router.callback_query(lambda x: x.data in ("enter_name", "you", "neutral_name"))
async def send_question_2(callback: CallbackQuery, state: FSMContext, language: str):
    await StartService(language).get_answer_on_start_question_1(
        callback=callback,
        state=state,
    )


@router.message(F.text, StartingStates.get_name)
async def get_user_name(message: Message, state: FSMContext, language: str):
    await StartService(language).get_user_name(message=message, state=state)


@router.callback_query(
    lambda x: x.data
    in ("calm_down", "sort_relationship", "inside_myself", "want_talk", "urgent")
)
async def send_question_3(callback: CallbackQuery, state: FSMContext, language: str):
    await StartService(language).get_answer_on_start_question_2(
        callback=callback,
        state=state,
    )


@router.message(F.voice | F.text, StartingStates.get_urgent_voice)
async def get_urgent_voice(message: Message, state: FSMContext, language: str):
    await StartService(language).from_start_question_to_just_talk(
        message=message,
        state=state,
        prompt_key="get_urgent_answer",
    )


@router.callback_query(StartingStates.get_feelings)
async def send_question_4(callback: CallbackQuery, state: FSMContext, language: str):
    await StartService(language).get_answer_on_start_question_3(
        callback=callback,
        state=state,
    )


@router.message(F.voice | F.text, StartingStates.get_complex_describe)
async def get_complex_describe(message: Message, state: FSMContext, language: str):
    await StartService(language).from_start_question_to_just_talk(
        message=message,
        state=state,
        prompt_key="get_complex_describe",
    )


@router.callback_query(
    lambda x: x.data
    in (
        "practice_methods",
        "analyze_situation",
        "history_other_peoples",
        "advice",
        "just_talking",
    )
)
async def after_question_4(callback: CallbackQuery, state: FSMContext, language: str):
    await StartService(language).after_question_4(callback=callback, state=state)


@router.message(F.text | F.voice, ChatStates.waiting_for_message)
async def just_chat(message: Message, state: FSMContext, language: str):
    await StartService(language).just_talk(message=message, state=state)
