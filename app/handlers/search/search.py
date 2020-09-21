import logging

from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold, hcode

from utils import *
from states import Search
from keyboards import home_keyboard, city_search_kb, like_and_more_kb, chat_and_more_kb
from database import db

log = logging.getLogger(__name__)


async def process_invalid_gender_search(message: types.Message):
    await message.delete()


async def process_gender_search(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(gender=query.data)
    await Search.next()
    await query.message.edit_text(hbold('🗺️Выберите город:'), reply_markup=city_search_kb(), parse_mode=ParseMode.HTML)


async def process_city_search_invalid(message: types.Message):
    await message.delete()


async def process_city_search(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if 'city_id' not in data.keys() or data['city_id'] != query.data:
            data['city_id'] = query.data
            data['offset'] = -1

        data['offset'] += 1
        user = db.next_user_by_city(data['city_id'], data['gender'], query.from_user.id, data['offset'])

        if not user and data['offset'] > 0:
            data['offset'] = 0
            user = db.next_user_by_city(data['city_id'], data['gender'], query.from_user.id, data['offset'])

        if not user:
            await query.message.answer(hbold('🤷‍️Тут пока никого нет, попробуйте позже'), parse_mode=ParseMode.HTML)
            await query.answer()
        else:
            await subtract_hearts(display_swipe, query.from_user.id, query, 1, user)


async def process_swipe_invalid(message: types.Message):
    await message.delete()


async def process_swipe(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['offset'] += 1
        except KeyError:
            data['offset'] = 0

        current_user = db.next_user_by_city(data['city_id'], data['gender'], query.from_user.id, data['offset'])

        if not current_user:
            await query.answer()
            await query.message.delete()
            data['offset'] = -1
            await query.message.answer(hbold('🏁Пока что всё, попробуйте ещё чуть позже😊'), parse_mode=ParseMode.HTML,
                                       reply_markup=home_keyboard())
        else:
            await subtract_hearts(display_swipe, query.from_user.id, query, 1, current_user)


async def display_swipe(query: types.CallbackQuery, user):
    await Search.swipes.set()
    await query.message.delete()
    await display_user(query.from_user.id, user, swipe=True)


async def process_like(query: types.CallbackQuery):
    to_user = extract_user_id(query.data)
    if db.liked(query.from_user.id, to_user):
        await query.answer('Вы уже лайкали этого человека!')
        return
    await subtract_hearts(send_like, query.from_user.id, query, 5, to_user)


async def send_like(query: types.CallbackQuery, user):
    db.add_like(query.from_user.id, user)
    is_free_profile = free_profile(query.from_user.id, user)
    if db.liked(user, query.from_user.id):  # if he liked me
        markup = chat_and_more_kb(parse_chat(query.from_user.id), parse_profile(query.from_user.id),
                                  free_profile=is_free_profile)
    else:
        markup = like_and_more_kb(parse_like(query.from_user.id), parse_profile(query.from_user.id),
                                  free_profile=is_free_profile)

    me = db.get_user_name(query.from_user.id)

    await Bot.get_current().send_message(user, hcode(f'Вас лайкнул пользователь {me}'),
                                         parse_mode=ParseMode.HTML, reply_markup=markup)
    await query.answer('Вы лайкнули этого человека!')


async def process_more(query: types.CallbackQuery):
    user_id = extract_user_id(query.data)
    chat = db.get_chat(query.from_user.id, user_id)
    if chat and db.is_chat_active(chat[0]):
        await send_profile(query, user_id)
    else:
        await subtract_hearts(send_profile, query.from_user.id, query, 5, user_id)


async def send_profile(query: types.CallbackQuery, user_id):
    user = db.get_user(user_id)
    await query.message.delete()
    await display_user(query.from_user.id, user)
    await query.answer()
