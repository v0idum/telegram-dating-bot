from aiogram import Bot, types
from aiogram.types import ParseMode

import strings
from database import db
from keyboards import like_and_chat_kb

import re


async def display_user(to_user, user, swipe=False, markup=None):
    keyboard = markup if markup is not None else like_and_chat_kb(parse_like(user[0]), parse_chat(user[0]), swipe=swipe)
    await Bot.get_current().send_photo(to_user, photo=user[6], caption=strings.user_info(user),
                                       reply_markup=keyboard, parse_mode=ParseMode.HTML)


def has_premium_or_hearts(user_id, number: int):
    if db.is_premium(user_id) or db.is_girl(user_id):  # It's free for girls ;)
        return True
    user_hearts = db.get_user_hearts(user_id)
    if user_hearts < number:
        return False
    new_value = user_hearts - number
    db.update_user_hearts(user_id, new_value)
    return new_value,


async def subtract_hearts(callback, user_id, query, hearts, *args):
    ok = has_premium_or_hearts(user_id, hearts)
    if ok:
        await show_subtract_answer(query, ok, hearts)
        await callback(query, *args)
    else:
        await query.answer(f'У вас недостаточно {strings.SYMBOL}')


async def show_subtract_answer(query: types.CallbackQuery, res, arg):
    if not isinstance(res, bool):
        await query.answer(f'-️{arg}{strings.SYMBOL} Осталось {res[0]}{strings.SYMBOL}')


def parse_gender(gender: str):
    return 1 if gender in (strings.MALE, strings.MALE_SEARCH) else 0


def parse_like(user_id):
    return ' '.join((strings.LIKE, str(user_id)))


def parse_chat(user_id):
    return ' '.join((strings.CHAT, str(user_id)))


def parse_profile(user_id):
    return ' '.join((strings.MORE, str(user_id)))


def is_like(callback_data: str):
    return callback_data.split()[0] == strings.LIKE


def is_chat(callback_data: str):
    return callback_data.split()[0] == strings.CHAT


def is_profile(callback_data: str):
    return callback_data.split()[0] == strings.MORE


def extract_user_id(data):
    return int(str(data).split()[1])


def extract_interlocutor(user_id, chat: tuple):
    return chat[0] if user_id == chat[1] else chat[1]


def free_profile(first_user_id, second_user_id):
    chat = db.get_chat(first_user_id, second_user_id)
    return db.is_chat_active(chat[0]) if chat else False


def is_cyrillic(text: str):
    return bool(re.search('^[а-яА-Я]+$', text))
