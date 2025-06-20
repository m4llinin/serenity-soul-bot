import asyncio
import random

from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
)

from src.utils.load_lexicon import LoaderLexicon
from src.keyboards.reply import ReplyKeyboard
from src.keyboards.inline import InlineKeyboard
from src.utils.uow import UOW
from src.states import (
    StartingStates,
    ChatStates,
)
from src.utils.ai_client import DeepseekClient
from src.utils.auido_converter import AudioConverter
from src.services.chat import ChatService


class StartService:
    def __init__(self, language: str = "ru") -> None:
        self.language = language
        self.texts = LoaderLexicon(language=self.language).load_messages()
        self.uow = UOW()

    async def get_partner_id(self, message_text: str, user_id: int) -> int | None:
        async with self.uow:
            split_text = message_text.split(" ")
            if len(split_text) == 2:
                partner_id = int(split_text[1])
                if partner_id != user_id:
                    referral = await self.uow.users.get_one({"id": partner_id})
                    if referral:
                        return partner_id

    async def start_message(self, message: Message, state: FSMContext) -> None:
        await state.set_state()
        async with self.uow:
            user = await self.uow.users.get_one({"id": message.chat.id})
            if user is None:
                partner_id = await self.get_partner_id(message.text, message.chat.id)
                user = await self.uow.users.insert(
                    {
                        "id": message.chat.id,
                        "partner_id": partner_id,
                    }
                )

            await message.answer(
                text=self.texts["start"],
                reply_markup=ReplyKeyboard(self.language).main(),
            )

            if user.is_first_start:
                await asyncio.sleep(0.5)
                await message.answer(
                    text=self.texts["start_question_1"],
                    reply_markup=InlineKeyboard(self.language).keyboard_column(
                        keys=["enter_name", "you", "neutral_name"],
                        callback_datas=["enter_name", "you", "neutral_name"],
                    ),
                )
                await self.uow.users.update(
                    filters={"id": message.chat.id},
                    data={"is_first_start": False},
                )

            await self.uow.commit()

    async def get_answer_on_start_question_1(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        chat_service = ChatService()
        chat_id = await chat_service.create_chat(
            user_id=callback.message.chat.id,
            chat_name="Стартовый",
        )
        await state.update_data(current_chat_id=chat_id)

        if callback.data == "enter_name":
            await state.set_state(StartingStates.get_name)
            await callback.message.edit_reply_markup(
                reply_markup=InlineKeyboard(self.language).keyboard_column(
                    keys=["entering"],
                    callback_datas=["None"],
                ),
            )
            return

        if callback.data == "neutral_name":
            names = LoaderLexicon(self.language).load_names()
            async with self.uow:
                await self.uow.users.update(
                    filters={"id": callback.message.chat.id},
                    data={"name": random.choice(names)},
                )
                await self.uow.commit()

        await callback.message.edit_text(
            text=self.texts["start_question_2"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=[
                    "calm_down",
                    "sort_relationship",
                    "inside_myself",
                    "urgent",
                    "want_talk",
                ],
                callback_datas=[
                    "calm_down",
                    "sort_relationship",
                    "inside_myself",
                    "urgent",
                    "want_talk",
                ],
            ),
        )

    async def get_user_name(self, message: Message, state: FSMContext) -> None:
        async with self.uow:
            await self.uow.users.update(
                filters={"id": message.chat.id},
                data={"name": message.text.strip()},
            )
            await self.uow.commit()
        await state.set_state(None)
        await message.answer(
            text=self.texts["start_question_2"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=[
                    "calm_down",
                    "sort_relationship",
                    "inside_myself",
                    "urgent",
                    "want_talk",
                ],
                callback_datas=[
                    "calm_down",
                    "sort_relationship",
                    "inside_myself",
                    "urgent",
                    "want_talk",
                ],
            ),
        )

    async def get_answer_on_start_question_2(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:

        if callback.data == "urgent":
            await state.set_state(StartingStates.get_urgent_voice)
            await callback.message.edit_reply_markup(
                reply_markup=InlineKeyboard(self.language).keyboard_column(
                    keys=["send_audio"],
                    callback_datas=["None"],
                ),
            )
            return

        await callback.message.edit_text(text=self.texts["wait_answer"])

        loader = LoaderLexicon(self.language)
        buttons = loader.load_keyboard()
        prompts = loader.load_prompts()
        theme = buttons[callback.data]

        chat_service = ChatService()
        chat_id = await state.get_value("current_chat_id")
        await chat_service.add_message(chat_id=chat_id, role="user", content=theme)

        client = DeepseekClient()
        feelings = await client.ask(prompts["get_feeling_on_theme"].format(theme=theme))
        updated_feelings = list(
            filter(
                lambda x: 0 < len(x) < 40,
                [i.strip().replace("**", "") for i in feelings.split("\n")],
            )
        )

        await chat_service.add_message(
            chat_id=chat_id,
            role="system",
            content=self.texts["start_question_3"],
        )

        await state.set_state(StartingStates.get_feelings)
        await callback.message.edit_text(
            text=self.texts["start_question_3"],
            reply_markup=InlineKeyboard(self.language).keyboard_column_with_texts(
                texts=updated_feelings + [buttons["complex_describe"]],
                callback_datas=updated_feelings + ["complex_describe"],
            ),
        )

    async def from_start_question_to_just_talk(
        self,
        message: Message,
        state: FSMContext,
        prompt_key: str,
    ) -> None:
        msg = await message.answer(text=self.texts["wait_answer"])

        if message.voice:
            text = await AudioConverter().get_text_from_voice(
                bot=message.bot,
                file_id=message.voice.file_id,
            )
        else:
            text = message.text

        chat_service = ChatService()
        chat_id = await state.get_value("current_chat_id")
        await chat_service.add_message(chat_id=chat_id, role="user", content=text)

        prompts = LoaderLexicon(self.language).load_prompts()
        client = DeepseekClient()
        answer = await client.ask(prompts[prompt_key].format(situation=text))

        await chat_service.add_message(chat_id=chat_id, role="system", content=answer)

        await state.set_state(ChatStates.waiting_for_message)
        await msg.edit_text(text=answer, parse_mode=ParseMode.MARKDOWN)

    async def get_answer_on_start_question_3(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        if callback.data == "complex_describe":
            await state.set_state(StartingStates.get_complex_describe)
            await callback.message.edit_text(
                text=self.texts["complex_describe"],
                reply_markup=InlineKeyboard(self.language).keyboard_column(
                    keys=["send_audio"],
                    callback_datas=["None"],
                ),
            )
            return

        chat_service = ChatService()
        chat_id = await state.get_value("current_chat_id")
        await chat_service.add_message(
            chat_id=chat_id, role="user", content=callback.data
        )

        await state.set_state(None)
        await callback.message.edit_text(
            text=self.texts["start_question_4"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=[
                    "practice_methods",
                    "analyze_situation",
                    "history_other_peoples",
                    "advice",
                    "just_talking",
                ],
                callback_datas=[
                    "practice_methods",
                    "analyze_situation",
                    "history_other_peoples",
                    "advice",
                    "just_talking",
                ],
            ),
        )

    async def after_question_4(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        await callback.message.edit_text(text=self.texts["wait_answer"])

        buttons = LoaderLexicon(self.language).load_keyboard()
        action = buttons[callback.data]
        chat_service = ChatService()
        chat_id = await state.get_value("current_chat_id")

        await chat_service.add_message(chat_id=chat_id, role="user", content=action)

        client = DeepseekClient()

        async with self.uow:
            messages = await self.uow.messages.get_all({"chat_id": chat_id})
            answer = await client.generate_response_from_history_messages(messages)

            await chat_service.add_message(
                chat_id=chat_id, role="system", content=answer
            )

            await state.set_state(ChatStates.waiting_for_message)
            await callback.message.edit_text(
                text=answer,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboard(self.language).keyboard_column(
                    keys=["can_continue_dialog"],
                    callback_datas=["None"],
                ),
            )

    async def just_talk(self, message: Message, state: FSMContext) -> None:
        msg = await message.answer(text=self.texts["wait_answer"])

        if message.voice:
            text = await AudioConverter().get_text_from_voice(
                bot=message.bot,
                file_id=message.voice.file_id,
            )
        else:
            text = message.text

        client = DeepseekClient()
        chat_service = ChatService()
        chat_id = await state.get_value("current_chat_id")

        await chat_service.add_message(chat_id=chat_id, role="user", content=text)

        async with self.uow:
            messages = await self.uow.messages.get_all({"chat_id": chat_id})
            answer = await client.generate_response_from_history_messages(messages)

            await chat_service.add_message(
                chat_id=chat_id, role="system", content=answer
            )

            await msg.edit_text(text=answer, parse_mode=ParseMode.MARKDOWN)
