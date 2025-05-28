from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from fastapi import FastAPI
from aiogram import (
    Bot,
    Dispatcher,
)
from contextlib import asynccontextmanager

from src.core.config import (
    WebhookConfig,
    TelegramConfig,
    RedisConfig,
)

from src.api.routers import router as api_router
from src.handlers.start import router as start_router
from src.handlers.menu import router as menu_router
from src.handlers.settings import router as settings_router
from src.handlers.profile import router as profile_router
from src.handlers.chat import router as chat_router
from src.middlewares.language import LanguageMiddleware


def setup_dispatcher():
    dp = Dispatcher(storage=RedisStorage(redis=RedisConfig().conn))

    dp.include_router(menu_router)
    dp.include_router(settings_router)
    dp.include_router(profile_router)
    dp.include_router(chat_router)
    dp.include_router(start_router)

    dp.update.middleware.register(LanguageMiddleware())
    return dp


@asynccontextmanager
async def lifespan(app: FastAPI):
    bot = Bot(
        token=TelegramConfig.TOKEN, default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = setup_dispatcher()

    await bot.set_webhook(
        url=WebhookConfig().URL,
        secret_token=WebhookConfig.SECRET,
        drop_pending_updates=True,
    )

    app.state.bot = bot
    app.state.dp = dp

    yield

    await bot.delete_webhook()
    await bot.session.close()


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
