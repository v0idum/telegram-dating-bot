from aiogram import Dispatcher

from utils import permitted
from .home import *
from strings import SEARCH, CONVERSE, PROFILE, BALANCE


def setup(dp: Dispatcher):
    dp.register_message_handler(handle_search, lambda message: permitted(message.from_user.id), text=SEARCH, state='*')
    dp.register_message_handler(process_chats, lambda message: permitted(message.from_user.id), text=CONVERSE,
                                state='*')
    dp.register_message_handler(process_balance, lambda message: permitted(message.from_user.id), text=BALANCE,
                                state='*')
    dp.register_message_handler(process_profile, lambda message: permitted(message.from_user.id), text=PROFILE,
                                state='*')
