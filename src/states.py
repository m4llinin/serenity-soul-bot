from aiogram.fsm.state import (
    StatesGroup,
    State,
)

JustTalking = State()


class StartingStates(StatesGroup):
    get_name = State()
    get_urgent_voice = State()
    get_feelings = State()
    get_voice = State()
    get_complex_describe = State()
