from aiogram import Dispatcher

from app.bot.handlers import routers


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.include_routers(*routers)
    return dispatcher
