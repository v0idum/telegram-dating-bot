from aiogram import Dispatcher

from config import ADMIN
from .admin import *


def setup(dp: Dispatcher):
    dp.register_message_handler(get_users, lambda message: str(message.from_user.id) in ADMIN, commands='users', state='*')
    dp.register_message_handler(remove_user, lambda message: str(message.from_user.id) in ADMIN, commands='rmuser', state='*')
    dp.register_message_handler(get_cities, lambda message: str(message.from_user.id) in ADMIN, commands='cities', state='*')
    dp.register_message_handler(remove_city, lambda message: str(message.from_user.id) in ADMIN, commands='rmcity', state='*')
    dp.register_message_handler(edit_users_city, lambda message: str(message.from_user.id) in ADMIN, commands='editcity', state='*')
