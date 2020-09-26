from aiogram import Dispatcher

from config import ADMIN
from .admin import *


def setup(dp: Dispatcher):
    dp.register_message_handler(remove_user, lambda message: message.from_user.id == ADMIN, commands='rmuser', state='*')
    dp.register_message_handler(get_users, lambda message: message.from_user.id == ADMIN, commands='users', state='*')
    dp.register_message_handler(remove_city, lambda message: message.from_user.id == ADMIN, commands='rmcity', state='*')
    dp.register_message_handler(edit_users_city, lambda message: message.from_user.id == ADMIN, commands='editcity', state='*')
