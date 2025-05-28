from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from src.utils.load_lexicon import LoaderLexicon


class ReplyKeyboard:
    def __init__(self, language: str = "ru"):
        self.texts = LoaderLexicon(language).load_keyboard()

    def main(self) -> ReplyKeyboardMarkup:
        kb = [
            [
                KeyboardButton(text=self.texts["my_profile"]),
                KeyboardButton(text=self.texts["settings"]),
            ],
            [
                KeyboardButton(text=self.texts["analyze"]),
                KeyboardButton(text=self.texts["my_chats"]),
            ],
            [
                KeyboardButton(text=self.texts["biblioteca"]),
                KeyboardButton(text=self.texts["subscription"]),
            ],
        ]
        return ReplyKeyboardMarkup(keyboard=kb)
