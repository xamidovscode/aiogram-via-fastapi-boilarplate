import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.settings import settings
from app.bot.runner import bot_runner
from app.bot.webhook import router as webhook_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    await bot_runner.start()
    yield
    await bot_runner.stop()


app = FastAPI(
    title='FastAPI Template',
    description='FastAPI project template',
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.include_router(webhook_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = {}
    for error in exc.errors():
        field = error["loc"][-1]
        errors[field] = error["msg"]
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "errors": errors
        }
    )


@app.get("/health")
async def health():
    return {"message": "OK"}
