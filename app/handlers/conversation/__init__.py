from .conversation import *
from ...states import Conversation
from ...utils import is_chat


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(process_chat_login, lambda query: is_chat(query.data), state='*')

    dp.register_message_handler(process_chatting, state=Conversation.room)
