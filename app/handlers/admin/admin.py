import logging

from aiogram import types
from database import db

logger = logging.getLogger(__name__)


async def remove_user(message: types.Message):
    user_id = message.get_args()
    if user_id and db.user_exists(user_id):
        db.remove_user(user_id)
        await message.answer(f'User {user_id} has been removed..')
        logger.info(f'User {user_id} has been removed..')
    else:
        await message.answer(f'User {user_id} does not exist')


async def get_users(message: types.Message):
    users = db.get_users()
    await message.answer(f'{len(users)}\n{users}')


async def remove_city(message: types.Message):
    name = message.get_args()
    if name and db.city_exists(name):
        db.remove_city(name)
        await message.answer(f'City {name} has been removed..')
        logger.info(f'City {name} has been removed..')
    else:
        await message.answer(f'City {name} does not exist')


async def edit_users_city(message: types.Message):
    cmd = message.get_args()
    if cmd:
        args = cmd.split(' ')
        db.edit_users_city_name(*args)
        await message.answer('Done')
