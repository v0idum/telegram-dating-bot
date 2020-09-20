from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold

from app.database import db
from app.states import EditProfile


async def handle_edit_btn(query: types.CallbackQuery):
    if query.data == EditProfile.name.state:
        await EditProfile.name.set()
        await Bot.get_current().send_message(query.from_user.id, 'Отправьте новое имя')
        await query.answer('Редактирование имени')
    elif query.data == EditProfile.age.state:
        await EditProfile.age.set()
        await Bot.get_current().send_message(query.from_user.id, 'Ваш возраст?')
        await query.answer('Изменение возраста')
    elif query.data == EditProfile.city.state:
        await EditProfile.city.set()
        await Bot.get_current().send_message(query.from_user.id, 'Отправьте название города (Кириллицей):')
        await query.answer('Изменение города')
    elif query.data == EditProfile.occupation.state:
        await EditProfile.occupation.set()
        await Bot.get_current().send_message(query.from_user.id, 'Ваш род занятий?')
        await query.answer('Редактирование рода занятий')
    elif query.data == EditProfile.about.state:
        await EditProfile.about.set()
        await Bot.get_current().send_message(query.from_user.id, 'Расскажите о себе!')
        await query.answer('Информация о себе')
    elif query.data == EditProfile.photo.state:
        await EditProfile.photo.set()
        await Bot.get_current().send_message(query.from_user.id, 'Отправьте новое фото:')
        await query.answer('Смена фото')


async def process_name(message: types.Message, state: FSMContext):
    db.update_user(message.from_user.id, 'name', message.text)
    await message.answer(bold('Ваше имя успешно изменено!'), parse_mode=ParseMode.MARKDOWN_V2)
    await state.reset_state(with_data=False)


async def process_age(message: types.Message, state: FSMContext):
    db.update_user(message.from_user.id, 'age', message.text)
    await message.answer(bold('Ваш возраст успешно изменён!'), parse_mode=ParseMode.MARKDOWN_V2)
    await state.reset_state(with_data=False)


async def process_city(message: types.Message, state: FSMContext):
    new_city_id = db.get_city_id(message.text)
    db.update_user(message.from_user.id, 'city', new_city_id)
    await message.answer(bold('Ваш город успешно изменён!'), parse_mode=ParseMode.MARKDOWN_V2)
    await state.reset_state(with_data=False)


async def process_occupation(message: types.Message, state: FSMContext):
    db.update_user(message.from_user.id, 'occupation', message.text)
    await message.answer(bold('Ваш род занятий успешно изменён!'), parse_mode=ParseMode.MARKDOWN_V2)
    await state.reset_state(with_data=False)


async def process_about(message: types.Message, state: FSMContext):
    db.update_user(message.from_user.id, 'about', message.text)
    await message.answer(bold('Информация о вас успешно сохранена!'), parse_mode=ParseMode.MARKDOWN_V2)
    await state.reset_state(with_data=False)


async def process_photo(message: types.Message, state: FSMContext):
    db.update_user(message.from_user.id, 'photo', message.photo[-1].file_id)
    await message.answer(bold('Ваше фото успешно сохранено!'), parse_mode=ParseMode.MARKDOWN_V2)
    await state.reset_state(with_data=False)
