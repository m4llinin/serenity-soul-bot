from fastapi import (
    APIRouter,
    Request,
)
from aiogram.types import Update

from src.core.config import (
    TelegramConfig,
    WebhookConfig,
)

router = APIRouter()


@router.post(WebhookConfig.PATH)
async def bot_webhook(request: Request):
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WebhookConfig.SECRET:
        return {"status": "forbidden"}

    update = Update.model_validate(
        await request.json(),
        context={"bot": TelegramConfig.bot},
    )
    await TelegramConfig.dp.feed_update(update)
    return {"status": "ok"}
