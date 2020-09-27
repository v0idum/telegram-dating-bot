import logging

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.markdown import *

from database import db
from keyboards import chat_and_more_kb, back_to_search_btn
from states import Conversation, Search
from utils import extract_user_id, parse_chat, parse_profile, free_profile, subtract_hearts


async def process_chat_login(query: types.CallbackQuery, state: FSMContext):
    with_user = extract_user_id(query.data)
    chat = db.get_chat(query.from_user.id, with_user)
    if not chat:
        db.create_chat(query.from_user.id, with_user)
        logging.info(f'New chat between {query.from_user.id} and {with_user} created')

    markup = None
    if await state.get_state() == Search.swipes.state:
        markup = back_to_search_btn()

    await Conversation.room.set()

    await state.update_data(interlocutor=with_user)
    name = db.get_user_name(with_user)
    await query.answer('Вход в чат')
    await query.message.delete()
    await query.message.answer(
        hbold(f'🗣️Вы перешли в чат с пользователем {name}. Он(а) получит все Ваши сообщения✈️.'),
        reply_markup=markup, parse_mode=ParseMode.HTML)


async def activate_chat_or_subtract(chat: tuple, message: types.Message, state: FSMContext):
    if chat[2] == message.from_user.id:  # Other user is creator of the chat
        db.activate_chat(chat[0])
        db.add_chat_to_user(chat[2], chat[0])
        logging.info(f'User {chat[2]} answered to user {chat[1]}')
        await deliver_message(message, state)
    else:
        await subtract_hearts(deliver_message, message.from_user.id, message, 10, state)


async def process_chatting(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        chat = db.get_chat(message.from_user.id, data['interlocutor'])
        if db.is_chat_active(chat[0]):
            await deliver_message(message, state)
        else:
            await activate_chat_or_subtract(chat, message, state)


async def deliver_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if db.is_fake(data['interlocutor']):
            print('Fake chatted')
            return
        with_user_state = Dispatcher.get_current().current_state(chat=data['interlocutor'], user=data['interlocutor'])
        async with with_user_state.proxy() as user_data:
            me = db.get_user_name(message.from_user.id)
            try:
                if user_data.state == Conversation.room.state and user_data['interlocutor'] == message.from_user.id:
                    await Bot.get_current().send_message(data['interlocutor'],
                                                         text(hbold(f'{me}:'), hitalic(message.text), sep='\n'),
                                                         parse_mode=ParseMode.HTML)
                else:
                    is_free_profile = free_profile(message.from_user.id, data['interlocutor'])
                    message.text = f'Сообщение от пользователя {me}:\n"{message.text}"'
                    await message.send_copy(data['interlocutor'],
                                            reply_markup=chat_and_more_kb(parse_chat(message.from_user.id),
                                                                          parse_profile(message.from_user.id),
                                                                          free_profile=is_free_profile))
            except BotBlocked:
                logging.warning(f"{me} could not chat with {data['interlocutor']}, user blocked the bot")
