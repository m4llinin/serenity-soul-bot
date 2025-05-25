from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from aiogram import (
    Bot,
    Dispatcher,
)

from src.core.config import (
    WebhookConfig,
    TelegramConfig,
)
from src.utils.load_lexicon import LoaderLexicon
from src.api.routers import router as webhook_router
from src.handlers.start import router as start_router


async def _on_startup(bot: Bot) -> None:
    texts = LoaderLexicon().load_messages()

    await bot.set_webhook(
        f"{WebhookConfig.BASE_URL}{WebhookConfig.PATH}",
        secret_token=WebhookConfig.SECRET,
        drop_pending_updates=True,
    )
    # await bot.set_my_description(description=texts["description"])
    # await bot.set_my_short_description(short_description=texts["short_description"])


async def _on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()


def main() -> None:
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.startup.register(_on_startup)
    dp.shutdown.register(_on_shutdown)

    bot = Bot(
        token=TelegramConfig.TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WebhookConfig.SECRET,
    )
    webhook_requests_handler.register(app, path=WebhookConfig.PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    # And finally start webserver
    web.run_app(app, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    main()
