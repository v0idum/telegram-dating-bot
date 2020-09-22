from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from strings import SEARCH, CONVERSE, PROFILE, BALANCE, NEXT, BACK, SYMBOL
from states import EditProfile


def gender_keyboard(male: str, female: str):
    markup = InlineKeyboardMarkup()
    male = InlineKeyboardButton(male, callback_data='1')
    female = InlineKeyboardButton(female, callback_data='0')
    markup.add(male, female)
    return markup


def request_contact_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    contact_btn = KeyboardButton('Отправить контакт', request_contact=True)
    markup.add(contact_btn)
    return markup


def home_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    search = KeyboardButton(SEARCH)
    conversation = KeyboardButton(CONVERSE)
    profile = KeyboardButton(PROFILE)
    balance = KeyboardButton(BALANCE)
    markup.add(search, conversation, profile, balance)
    return markup


def city_search_kb():
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(*(InlineKeyboardButton(callback_data=city_row[0], text=city_row[1]) for city_row in db.get_cities()))
    return kb


def like_and_chat_kb(like: str, chat: str, swipe=False):
    kb = InlineKeyboardMarkup()
    like = InlineKeyboardButton(f'👍🏻 5{SYMBOL}', callback_data=like)
    send_message = InlineKeyboardButton(f'✉️ 10{SYMBOL}', callback_data=chat)
    buttons = [like, send_message]
    if swipe:
        nxt = InlineKeyboardButton(f'➡️ 1{SYMBOL}', callback_data=NEXT)
        buttons.append(nxt)
    kb.add(*buttons)
    return kb


def back_to_search_btn():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(BACK, callback_data=NEXT))
    return kb


def like_and_more_kb(like: str, more: str, free_profile=False):
    kb = InlineKeyboardMarkup()
    profile_text = '✅Профиль' if free_profile else f'👁Профиль 5{SYMBOL}'
    kb.add(InlineKeyboardButton(f'👍🏻 5{SYMBOL}', callback_data=like), InlineKeyboardButton(profile_text, callback_data=more))
    return kb


def chat_and_more_kb(chat: str, more: str, free_profile=False):
    kb = InlineKeyboardMarkup()
    profile_text = '✅Профиль' if free_profile else f'👁Профиль 5{SYMBOL}'
    chat_text = '✉Написать' if free_profile else f'✉ 10{SYMBOL}'
    kb.add(InlineKeyboardButton(chat_text, callback_data=chat), InlineKeyboardButton(profile_text, callback_data=more))
    return kb


def chat_kb(chat: str):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('✉️Написать', callback_data=chat))
    return kb


def profile_edit_kb():
    kb = InlineKeyboardMarkup()
    name = InlineKeyboardButton('📋Имя', callback_data=EditProfile.name.state)
    age = InlineKeyboardButton('📅Возраст', callback_data=EditProfile.age.state)
    city = InlineKeyboardButton('🗺️Город', callback_data=EditProfile.city.state)
    occupation = InlineKeyboardButton('🎭Род занятий', callback_data=EditProfile.occupation.state)
    about = InlineKeyboardButton('📝О себе', callback_data=EditProfile.about.state)
    photo = InlineKeyboardButton('📷Фото', callback_data=EditProfile.photo.state)
    kb.add(name, age, city, occupation, about, photo)
    return kb
