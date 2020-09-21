import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.utils import executor
from app.handlers import registration, home, search, conversation, editprofile
from aiogram import types
from app.config import BOT_TOKEN, ADMIN
from app.database import db

logging.basicConfig(level=logging.INFO, filename='logs.log')

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(bot, storage=JSONStorage('states.json'))


async def shutdown_storage(dispatcher: Dispatcher):
    db.close()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


@dp.message_handler(lambda message: message.from_user.id == ADMIN, commands='rmuser', state='*')
async def remove_user(message: types.Message):
    user_id = message.get_args()
    if user_id and db.user_exists(user_id):
        db.remove_user(user_id)
        await message.answer(f'User {user_id} has been removed..')
        logging.info(f'User {user_id} has been removed..')
    else:
        await message.answer(f'User {user_id} does not exist')


@dp.message_handler(lambda message: message.from_user.id == ADMIN, commands='all', state='*')
async def get_users(message: types.Message):
    await message.answer(db.get_users())


if __name__ == '__main__':
    home.setup(dp)
    registration.setup(dp)
    conversation.setup(dp)
    search.setup(dp)
    editprofile.setup(dp)
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown_storage)
