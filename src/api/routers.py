from fastapi import (
    APIRouter,
    Request,
)
from aiogram.types import Update

from src.core.config import WebhookConfig

router = APIRouter()


@router.post(WebhookConfig.PATH)
async def bot_webhook(request: Request):
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WebhookConfig.SECRET:
        return {"status": "forbidden"}

    bot = request.app.state.bot
    dp = request.app.state.dp

    update = Update.model_validate(await request.json())
    await dp.feed_update(bot=bot, update=update)

    return {"status": "ok"}


@router.get("/health")
async def health():
    return {"status": "ok"}
