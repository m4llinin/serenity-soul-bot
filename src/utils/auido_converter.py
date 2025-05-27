import os
import json

from aiogram import Bot
from loguru import logger
from pydub import AudioSegment
import speech_recognition as sr


class AudioConverter:
    def __init__(self):
        self.r = sr.Recognizer()

    @staticmethod
    def convert_ogg_to_wav(input_file: str, output_file: str) -> None:
        ogg_audio = AudioSegment.from_ogg(input_file)
        ogg_audio.export(output_file, format="wav")

    def recognize_speech(self, audio_file: str) -> str:
        with sr.AudioFile(audio_file) as source:
            audio_data = self.r.record(source)
            self.r.adjust_for_ambient_noise(source)

        try:
            text = self.r.recognize_vosk(audio_data, language="ru")
            return json.loads(text)["text"]
        except sr.UnknownValueError as e:
            raise ValueError(f"Не удалось распознать речь: {e}")
        except sr.RequestError as e:
            raise ConnectionError(f"Ошибка сервиса распознавания: {e}")

    @staticmethod
    async def download_voice(bot: Bot, file_id: str) -> tuple[str, str] | None:
        try:
            file = await bot.get_file(file_id)
            file_path = file.file_path

            ogg_file = f"temp/{file_id}.ogg"
            wav_file = f"temp/{file_id}.wav"

            await bot.download_file(file_path, ogg_file)
            return ogg_file, wav_file
        except Exception as e:
            logger.error(f"Error downloading voice file {file_id}: {e}")
            return

    @staticmethod
    def delete_voice(ogg_file: str, wav_file: str) -> None:
        os.remove(ogg_file)
        os.remove(wav_file)

    async def get_text_from_voice(self, bot: Bot, file_id: str) -> str:
        ogg_file, wav_file = await self.download_voice(bot=bot, file_id=file_id)
        self.convert_ogg_to_wav(ogg_file, wav_file)
        text = self.recognize_speech(wav_file)
        self.delete_voice(ogg_file, wav_file)
        return text
