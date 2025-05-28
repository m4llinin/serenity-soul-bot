from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.keyboards.inline import InlineKeyboard
from src.utils.load_lexicon import LoaderLexicon
from src.utils.uow import UOW


class SettingsService:
    def __init__(self, language: str = "ru") -> None:
        self.language = language
        self.texts = LoaderLexicon(language=self.language).load_messages()
        self.uow = UOW()

    async def settings_menu(self, message: Message, state: FSMContext) -> None:
        await state.set_state()
        await message.answer(
            text=self.texts["settings"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=["model", "communication_style", "language"],
                callback_datas=["model", "communication_style", "language"],
            ),
        )

    async def choose_model(self, callback: CallbackQuery) -> None:
        await callback.message.edit_text(
            text=self.texts["choose_model"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=["short", "pretty", "strict", "light", "back"],
                callback_datas=["short", "pretty", "strict", "light", "settings"],
            ),
        )

    async def get_chosen_model(self, callback: CallbackQuery) -> None:
        buttons = LoaderLexicon(self.language).load_keyboard()
        await callback.answer(
            text=self.texts["get_chosen"].format(model=buttons[callback.data]),
            show_alert=True,
        )

    async def choose_communication_style(self, callback: CallbackQuery) -> None:
        await callback.message.edit_text(
            text=self.texts["choose_model"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=["friend", "teacher", "neutral", "back"],
                callback_datas=["friend", "teacher", "neutral", "settings"],
            ),
        )

    async def get_chosen_communication_style(self, callback: CallbackQuery) -> None:
        async with self.uow:
            await self.uow.users.update(
                filters={"id": callback.message.chat.id},
                data={"communication_style": callback.data},
            )
            await self.uow.commit()

        buttons = LoaderLexicon(self.language).load_keyboard()
        await callback.answer(
            text=self.texts["get_chosen"].format(model=buttons[callback.data]),
            show_alert=True,
        )

    async def choose_language(self, callback: CallbackQuery) -> None:
        buttons = LoaderLexicon(self.language).load_keyboard()
        await callback.message.edit_text(
            text=self.texts["choose_model"],
            reply_markup=InlineKeyboard(self.language).keyboard_column_with_texts(
                texts=LoaderLexicon(self.language).get_languages + [buttons["back"]],
                callback_datas=LoaderLexicon(self.language).get_languages
                + ["settings"],
            ),
        )

    async def get_chosen_language(self, callback: CallbackQuery) -> None:
        async with self.uow:
            await self.uow.users.update(
                filters={"id": callback.message.chat.id},
                data={"language": callback.data},
            )
            await self.uow.commit()

        await callback.answer(
            text=self.texts["get_chosen"].format(model=callback.data),
            show_alert=True,
        )
