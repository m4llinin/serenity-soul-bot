import os

from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.client.default import DefaultBotProperties
from redis.asyncio import Redis

load_dotenv()


class RedisConfig:
    HOST: str = os.getenv("REDIS_HOST")
    PORT: str = os.getenv("REDIS_PORT")
    DB: str = os.getenv("REDIS_DB")

    @property
    def URL(self) -> str:
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"

    @property
    def conn(self) -> Redis:
        return Redis.from_url(
            self.URL,
            single_connection_client=True,
        )


class DBConfig:
    PATH: str = os.getenv("DB_PATH")

    def URL(self, migrations: bool = False) -> str:
        if migrations:
            return f"sqlite:///{self.PATH}"
        return f"sqlite+aiosqlite:///{self.PATH}"


class WebhookConfig:
    BASE_URL: str = os.getenv("BASE_WEBHOOK_URL")
    PATH: str = os.getenv("WEBHOOK_PATH")
    SECRET: str = os.getenv("WEBHOOK_SECRET")

    @property
    def URL(self) -> str:
        return f"{self.BASE_URL}{self.PATH}"


class TelegramConfig:
    TOKEN = os.getenv("API_TOKEN")
    ADMIN_CHAT = os.getenv("ADMIN_CHAT")


class AIConfig:
    DEEPSEEK_TOKEN: str = os.getenv("DEEPSEEK_TOKEN")
