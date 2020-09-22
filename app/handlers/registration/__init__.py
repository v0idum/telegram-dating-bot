from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types.message import ContentType

from .registration import *
from states import Profile
from utils import is_cyrillic


def setup(dp: Dispatcher):
    dp.register_message_handler(cmd_start, CommandStart(), state='*')

    dp.register_message_handler(process_invalid_name, lambda message: len(message.text) > 25, state=Profile.name)
    dp.register_message_handler(process_name, state=Profile.name)

    dp.register_message_handler(process_age_invalid, lambda message: not message.text.isdigit(), state=Profile.age)
    dp.register_message_handler(process_age, lambda message: message.text.isdigit(), state=Profile.age)

    dp.register_message_handler(process_gender_invalid, state=Profile.gender)
    dp.register_callback_query_handler(process_gender, lambda query: query.data in ('1', '0'), state=Profile.gender)

    dp.register_message_handler(process_city_invalid, lambda message: not is_cyrillic(message.text), state=Profile.city)
    dp.register_message_handler(process_city, lambda message: is_cyrillic(message.text), state=Profile.city)

    dp.register_message_handler(process_occupation, state=Profile.occupation)

    dp.register_message_handler(process_about, state=Profile.about)

    dp.register_message_handler(process_photo_and_save_data, state=Profile.photo, content_types=ContentType.PHOTO)
    dp.register_message_handler(process_invalid_photo, state=Profile.photo, content_types=ContentType.ANY)
