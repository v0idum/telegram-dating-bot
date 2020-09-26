import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.utils import executor
from handlers import registration, home, search, conversation, editprofile
from config import BOT_TOKEN
from database import db

logging.basicConfig(level=logging.INFO, filename='logs.log')

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(bot, storage=JSONStorage('states.json'))


async def shutdown_storage(dispatcher: Dispatcher):
    db.close()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    home.setup(dp)
    registration.setup(dp)
    conversation.setup(dp)
    search.setup(dp)
    editprofile.setup(dp)
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown_storage)
