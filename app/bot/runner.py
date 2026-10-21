import asyncio
import logging
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.types import Update

from app.bot.dispatcher import create_dispatcher
from app.core.settings import settings

logger = logging.getLogger(__name__)


class BotRunner:
    def __init__(self) -> None:
        self.bot: Bot | None = None
        self.dispatcher: Dispatcher | None = None
        self.task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        if not settings.BOT_TOKEN:
            logger.warning("BOT_TOKEN is not configured; Telegram polling is disabled")
            return

        webhook_url = self.webhook_url if settings.BOT_MODE == "webhook" else None
        self.bot = Bot(token=settings.BOT_TOKEN)
        self.dispatcher = create_dispatcher()
        allowed_updates = self.dispatcher.resolve_used_update_types()

        if settings.BOT_MODE == "webhook":
            await self.bot.set_webhook(
                url=webhook_url,
                allowed_updates=allowed_updates,
                secret_token=settings.WEBHOOK_SECRET,
            )
            return

        await self.bot.delete_webhook(drop_pending_updates=False)
        self.task = asyncio.create_task(
            self.dispatcher.start_polling(
                self.bot,
                allowed_updates=allowed_updates,
                close_bot_session=False,
            )
        )

    async def stop(self) -> None:
        if self.dispatcher and self.dispatcher.is_polling():
            await self.dispatcher.stop_polling()

        if self.task:
            if not self.task.done():
                self.task.cancel()

            try:
                await self.task
            except asyncio.CancelledError:
                pass

        if self.bot:
            await self.bot.session.close()

        self.task = None
        self.dispatcher = None
        self.bot = None

    @property
    def webhook_url(self) -> str:
        if not settings.WEBHOOK_BASE_URL:
            raise RuntimeError("WEBHOOK_BASE_URL is required when BOT_MODE=webhook")

        url = f"{settings.WEBHOOK_BASE_URL.rstrip('/')}/{settings.WEBHOOK_PATH.lstrip('/')}"
        if not url.startswith("https://"):
            raise RuntimeError("WEBHOOK_BASE_URL must use HTTPS")

        return url

    async def handle_webhook(self, payload: dict[str, Any]) -> None:
        if not self.bot or not self.dispatcher:
            raise RuntimeError("Telegram bot is not running")

        update = Update.model_validate(payload, context={"bot": self.bot})
        await self.dispatcher.feed_update(self.bot, update)


bot_runner = BotRunner()
