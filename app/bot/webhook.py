from hmac import compare_digest

from fastapi import APIRouter, Header, HTTPException, Request, status

from app.bot.runner import bot_runner
from app.core.settings import settings

router = APIRouter(include_in_schema=False)


@router.post(settings.WEBHOOK_PATH)
async def telegram_webhook(
    request: Request,
    secret_token: str | None = Header(
        default=None,
        alias="X-Telegram-Bot-Api-Secret-Token",
    ),
):
    if settings.BOT_MODE != "webhook":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if settings.WEBHOOK_SECRET and (
        not secret_token or not compare_digest(secret_token, settings.WEBHOOK_SECRET)
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    try:
        await bot_runner.handle_webhook(await request.json())
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error

    return {"ok": True}
