from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.utils.load_lexicon import LoaderLexicon


class InlineKeyboard:
    def __init__(self, language: str = "ru"):
        self.texts = LoaderLexicon(language).load_keyboard()

    def keyboard_column(
        self,
        keys: list[str],
        callback_datas: list[str],
    ) -> InlineKeyboardMarkup:
        kb = []

        if len(keys) != len(callback_datas):
            raise IndexError("length of keys is not equal to length of callback datas")

        for key, callback_data in zip(keys, callback_datas):
            kb.append(
                [
                    InlineKeyboardButton(
                        text=self.texts[key], callback_data=callback_data
                    )
                ]
            )

        return InlineKeyboardMarkup(inline_keyboard=kb)

    @staticmethod
    def keyboard_column_with_texts(
        texts: list[str],
        callback_datas: list[str],
    ) -> InlineKeyboardMarkup:
        kb = []

        if len(texts) != len(callback_datas):
            raise IndexError("length of keys is not equal to length of callback datas")

        for key, callback_data in zip(texts, callback_datas):
            kb.append([InlineKeyboardButton(text=key, callback_data=callback_data)])

        return InlineKeyboardMarkup(inline_keyboard=kb)

    def partner(self, user_id: int):
        kb = [
            [
                InlineKeyboardButton(
                    text=self.texts["share_link"],
                    url=f"https://t.me/share/url?url=https://t.me/SerenitySoul_bot?start={user_id}",
                )
            ],
            [InlineKeyboardButton(text=self.texts["back"], callback_data="my_profile")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=kb)
