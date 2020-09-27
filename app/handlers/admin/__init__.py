from aiogram import Dispatcher
from aiogram.types import ContentType

from config import ADMIN
from .admin import *
from states import FakeUser


def setup(dp: Dispatcher):
    dp.register_message_handler(get_users, lambda message: str(message.from_user.id) in ADMIN, commands='users', state='*')
    dp.register_message_handler(remove_user, lambda message: str(message.from_user.id) in ADMIN, commands='rmuser', state='*')
    dp.register_message_handler(get_cities, lambda message: str(message.from_user.id) in ADMIN, commands='cities', state='*')
    dp.register_message_handler(remove_city, lambda message: str(message.from_user.id) in ADMIN, commands='rmcity', state='*')
    dp.register_message_handler(edit_users_city, lambda message: str(message.from_user.id) in ADMIN, commands='editcity', state='*')

    dp.register_message_handler(add_fake, lambda message: str(message.from_user.id) in ADMIN, commands='fake', state='*')

    dp.register_message_handler(process_name, lambda message: str(message.from_user.id) in ADMIN, state=FakeUser.name)
    dp.register_message_handler(process_age, lambda message: str(message.from_user.id) in ADMIN, state=FakeUser.age)
    dp.register_callback_query_handler(process_gender, lambda query: str(query.from_user.id) in ADMIN, state=FakeUser.gender)
    dp.register_message_handler(process_city, lambda message: str(message.from_user.id) in ADMIN, state=FakeUser.city)
    dp.register_message_handler(process_occupation, lambda message: str(message.from_user.id) in ADMIN, state=FakeUser.occupation)
    dp.register_message_handler(process_about, lambda message: str(message.from_user.id) in ADMIN, state=FakeUser.about)
    dp.register_message_handler(process_save, lambda message: str(message.from_user.id) in ADMIN, state=FakeUser.photo, content_types=ContentType.ANY)
