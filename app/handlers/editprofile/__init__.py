from aiogram import Dispatcher
from .edition import *
from aiogram.types.message import ContentType

from states import EditProfile
from handlers.registration.registration import process_invalid_name, process_age_invalid, process_invalid_photo, process_city_invalid
from utils import is_cyrillic


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(handle_edit_btn, state='*')

    dp.register_message_handler(process_invalid_name, lambda message: len(message.text) > 25, state=EditProfile.name)
    dp.register_message_handler(process_name, lambda message: len(message.text) <= 25, state=EditProfile.name)

    dp.register_message_handler(process_age_invalid, lambda message: not message.text.isdigit(), state=EditProfile.age)
    dp.register_message_handler(process_age, lambda message: message.text.isdigit(), state=EditProfile.age)

    dp.register_message_handler(process_city_invalid, lambda message: not is_cyrillic(message.text), state=EditProfile.city)
    dp.register_message_handler(process_city, lambda message: is_cyrillic(message.text), state=EditProfile.city)

    dp.register_message_handler(process_occupation, state=EditProfile.occupation)

    dp.register_message_handler(process_about, state=EditProfile.about)

    dp.register_message_handler(process_photo, state=EditProfile.photo, content_types=ContentType.PHOTO)
    dp.register_message_handler(process_invalid_photo, state=EditProfile.photo, content_types=ContentType.ANY)
