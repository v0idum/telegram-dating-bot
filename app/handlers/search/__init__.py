from aiogram import Dispatcher
from aiogram.types import ContentType

from .search import *
from app.strings import MALE_SEARCH, FEMALE_SEARCH, NEXT
from app.states import Search
from app.utils import is_like, is_chat, is_profile


def setup(dp: Dispatcher):
    dp.register_message_handler(process_invalid_gender_search, state=Search.gender)
    dp.register_callback_query_handler(process_gender_search, lambda query: query.data in ('1', '0'), state=Search.gender)

    dp.register_message_handler(process_city_search_invalid, state=Search.city, content_types=ContentType.ANY)
    dp.register_callback_query_handler(process_city_search, state=Search.city)

    dp.register_message_handler(process_swipe_invalid, state=Search.swipes, content_types=ContentType.ANY)
    dp.register_callback_query_handler(process_swipe, lambda query: query.data == NEXT, state='*')

    dp.register_callback_query_handler(process_like, lambda query: is_like(query.data), state='*')

    dp.register_callback_query_handler(process_more, lambda query: is_profile(query.data), state='*')
