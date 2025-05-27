from aiogram.fsm.state import (
    StatesGroup,
    State,
)


class StartingStates(StatesGroup):
    get_name = State()
    get_urgent_voice = State()
    get_feelings = State()
    get_voice = State()
    get_complex_describe = State()


class SupportStates(StatesGroup):
    get_improvement_message = State()
    get_support_message = State()
    get_support_reply = State()


class ChatStates(StatesGroup):
    waiting_for_message = State()
    waiting_for_chat_name = State()
