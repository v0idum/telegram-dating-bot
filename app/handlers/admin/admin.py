import logging

from aiogram import types
from aiogram.dispatcher import FSMContext


from database import db
from states import FakeUser
from keyboards import gender_keyboard
from utils import is_cyrillic, random_id

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


async def get_cities(message: types.Message):
    cities = db.get_cities()
    await message.answer(f'{len(cities)}\n{cities}')


async def add_fake(message: types.Message):
    await message.answer('Добавление фейка.')

    await FakeUser.name.set()
    await message.answer('Имя:')


async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Возраст:')
    await FakeUser.next()


async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Возраст должен состоять только из цифр, введите занова!')
        return
    await state.update_data(age=message.text)
    await message.answer('Пол:', reply_markup=gender_keyboard())
    await FakeUser.next()


async def process_gender(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(gender=query.data)
    await query.message.delete()
    await query.message.answer('Город:')
    await FakeUser.next()


async def process_city(message: types.Message, state: FSMContext):
    if not is_cyrillic(message.text):
        await message.answer('Город должен быть на кириллице, попробуйте ещё разок!')
        return
    await state.update_data(city=db.get_city_id(message.text))
    await message.answer('Род занятий:')
    await FakeUser.next()


async def process_occupation(message: types.Message, state: FSMContext):
    await state.update_data(occupation=message.text)
    await message.answer('О себе:')
    await FakeUser.next()


async def process_about(message: types.Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer('Фото:')
    await FakeUser.next()


async def process_save(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer('Отправьте валидное фото')
    async with state.proxy() as data:
        db.add_fake(random_id(), data['name'], data['age'],
                    data['gender'], data['city'], data['occupation'],
                    data['about'], message.photo[-1].file_id)
        await state.finish()
        await message.answer('Фейк добавлен. Нажмите /fake чтобы добавить ещё')
