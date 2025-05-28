import os
from datetime import datetime
from pathlib import Path

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
    FSInputFile,
)
from fpdf import FPDF
from loguru import logger

from src.keyboards.inline import InlineKeyboard
from src.utils.load_lexicon import LoaderLexicon
from src.utils.uow import UOW
from src.states import ChatStates


class ChatService:
    def __init__(self, language: str = "ru") -> None:
        self.language = language
        self.texts = LoaderLexicon(language=self.language).load_messages()
        self.uow = UOW()

    async def my_chats(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        await state.set_state()
        await message.answer(
            text=self.texts["my_chats"],
            reply_markup=InlineKeyboard(self.language).keyboard_column(
                keys=[
                    "create_chat",
                    "find_message",
                    "export_dialog",
                    "your_chats",
                ],
                callback_datas=[
                    "create_chat",
                    "find_message",
                    "export_dialog",
                    "your_chats",
                ],
            ),
        )

    async def send_message_create_chat(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        await state.set_state(ChatStates.waiting_for_chat_name)
        await callback.message.edit_text(text=self.texts["message_create_chat"])

    async def get_chat_name(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        try:
            async with self.uow:
                await self.uow.chats.insert(
                    {
                        "user_id": message.chat.id,
                        "chat_name": message.text,
                    }
                )
                await self.uow.commit()
            await message.answer(
                text=self.texts["get_chat_name"].format(message.text),
                reply_markup=InlineKeyboard(self.language).keyboard_column(
                    keys=["ready"],
                    callback_datas=["my_chats"],
                ),
            )
        except Exception as e:
            logger.error(e)
            await message.answer(
                text=self.texts["error_get_chat_name"],
                reply_markup=InlineKeyboard(self.language).keyboard_column(
                    keys=["back"],
                    callback_datas=["my_chats"],
                ),
            )
        await state.set_state(None)

    async def choose_current_chat(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        buttons = LoaderLexicon(language=self.language).load_keyboard()
        async with self.uow:
            chats = await self.uow.chats.get_all({"user_id": callback.message.chat.id})
            current_chat_id = (await state.get_value("current_chat_id")) or 0
            current_chat = await self.uow.chats.get_one({"id": current_chat_id})

            await callback.message.edit_text(
                text=self.texts["choose_current_chat"].format(
                    current_chat.chat_name if current_chat else self.texts["not_select"]
                ),
                reply_markup=InlineKeyboard(self.language).keyboard_column_with_texts(
                    texts=[chat.chat_name for chat in chats] + [buttons["back"]],
                    callback_datas=[f"choose_chat_{chat.id}" for chat in chats]
                    + ["my_chats"],
                ),
            )

    async def set_current_chat(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        chat_id = int(callback.data.split("_")[2])
        await state.update_data(current_chat_id=chat_id)
        async with self.uow:
            chats = await self.uow.chats.get_all({"user_id": callback.message.chat.id})
            chat = await self.uow.chats.get_one({"id": chat_id})
            buttons = LoaderLexicon(language=self.language).load_keyboard()

            try:
                await callback.message.edit_text(
                    text=self.texts["choose_current_chat"].format(chat.chat_name),
                    reply_markup=InlineKeyboard(
                        self.language
                    ).keyboard_column_with_texts(
                        texts=[chat.chat_name for chat in chats] + [buttons["back"]],
                        callback_datas=[f"choose_chat_{chat.id}" for chat in chats]
                        + ["my_chats"],
                    ),
                )
            except:
                pass

    async def export_chat_to_pdf(
        self,
        callback: CallbackQuery,
        state: FSMContext,
    ) -> None:
        try:
            await callback.answer(
                text=self.texts["start_exporting"],
                show_alert=True,
            )

            current_chat_id = await state.get_value("current_chat_id")
            if not current_chat_id:
                await callback.message.edit_text(
                    text=self.texts["no_chat_selected"],
                )
                return

            async with self.uow:
                chat = await self.uow.chats.get_one({"id": current_chat_id})
                messages = await self.uow.messages.get_all({"chat_id": current_chat_id})

                pdf = FPDF()

                font_added = False
                font = "DejaVu"

                try:
                    project_root = Path(__file__).parent.parent.parent

                    custom_font_paths = [
                        project_root / "fonts" / "NotoSans-Regular.ttf",
                        project_root / "fonts" / "NotoSans-Bold.ttf",
                    ]

                    if all(path.exists() for path in custom_font_paths):
                        # Add regular font
                        pdf.add_font(
                            "CustomFont",
                            style="",
                            fname=str(custom_font_paths[0]),
                            uni=True,
                        )

                        # Add bold font
                        pdf.add_font(
                            "CustomFont",
                            style="B",
                            fname=str(custom_font_paths[1]),
                            uni=True,
                        )

                        font = "CustomFont"
                        font_added = True

                    # If custom fonts not found, try system fonts based on platform
                    if not font_added:
                        system_fonts = [
                            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                        ]
                        font = "DejaVu"

                        if system_fonts and all(
                            os.path.exists(path) for path in system_fonts
                        ):
                            pdf.add_font(
                                font, style="", fname=system_fonts[0], uni=True
                            )
                            pdf.add_font(
                                font, style="B", fname=system_fonts[1], uni=True
                            )
                            font_added = True

                except Exception as font_error:
                    logger.error(f"Error adding custom font: {font_error}")

                if not font_added:
                    font = "Helvetica"
                    logger.warning(
                        "Using built-in Helvetica font. Unicode characters may not display correctly."
                    )

                pdf.set_font(font, size=10)

                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)

                # Add title
                pdf.set_font(font, size=16)
                pdf.cell(0, 10, f"Chat: {chat.chat_name}.", ln=True, align="C")
                pdf.ln(5)

                # Add export date
                pdf.set_font(font, size=10)
                export_date = datetime.now().strftime("%H:%M:%S %Y-%m-%d")
                pdf.cell(0, 10, f"Export date: {export_date}", ln=True, align="R")
                pdf.ln(5)

                # Add messages
                pdf.set_font(font, size=10)
                for message in messages:
                    timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")

                    if message.role == "user":
                        pdf.set_text_color(0, 0, 255)  # Blue for user
                        role_text = "You"
                    else:
                        pdf.set_text_color(0, 128, 0)  # Green for assistant
                        role_text = "System"

                    pdf.set_font(font, style="B", size=10)  # Bold for header
                    pdf.cell(0, 10, f"{role_text} - {timestamp}", ln=True)

                    pdf.set_font(font, size=10)

                    pdf.multi_cell(0, 10, message.content)
                    pdf.ln(5)

                pdf.set_text_color(0, 0, 0)

                export_dir = "./temp"
                safe_chat_name = "".join(
                    c if c.isalnum() else "_" for c in chat.chat_name
                )
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{export_dir}/chat_{safe_chat_name}_{timestamp}.pdf"
                pdf.output(filename)

                await callback.answer(
                    text=self.texts["export_success"],
                    show_alert=True,
                )
                await callback.message.answer_document(
                    document=FSInputFile(path=filename)
                )
                os.remove(filename)

        except Exception as e:
            logger.error(f"Error exporting chat to PDF: {e}")
            await callback.answer(text=self.texts["export_error"], show_alert=True)
            return None

    async def create_chat(self, user_id: int, chat_name: str) -> int:
        async with self.uow:
            chat = await self.uow.chats.insert(
                {
                    "user_id": user_id,
                    "chat_name": chat_name,
                }
            )
            await self.uow.commit()
            return chat.id

    async def add_message(self, chat_id: str, role: str, content: str) -> None:
        async with self.uow:
            await self.uow.messages.insert(
                {
                    "chat_id": chat_id,
                    "role": role,
                    "content": content,
                }
            )
            await self.uow.commit()
