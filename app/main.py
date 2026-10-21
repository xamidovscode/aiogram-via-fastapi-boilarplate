import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(
    title='FastAPI Template',
    description='FastAPI project template',
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
