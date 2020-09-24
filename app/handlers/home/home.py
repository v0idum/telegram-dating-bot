import logging

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram.utils.markdown import *

from database import db
from states import Search, Conversation, EditProfile
from keyboards import gender_keyboard, home_keyboard, chat_kb, profile_edit_kb
import strings
from config import INVITE_LINK
from utils import extract_interlocutor, display_user, parse_chat

log = logging.getLogger(__name__)


async def handle_search(message: types.Message):
    await Search.gender.set()
    await message.answer(hbold('Кого Вы хотите найти❓'),
                         parse_mode=ParseMode.HTML,
                         reply_markup=gender_keyboard(strings.MALE_SEARCH, strings.FEMALE_SEARCH))


async def process_chats(message: types.Message):
    await Conversation.chats.set()
    me = message.from_user.id
    chats = db.get_chats_of_user(me)
    if not chats:
        await message.answer(hbold('У Вас пока нет собеседников🥺'), parse_mode=ParseMode.HTML)
    else:
        for chat in chats:
            interlocutor = db.get_user(extract_interlocutor(me, chat))
            await display_user(me, interlocutor, markup=chat_kb(parse_chat(interlocutor[0])))
        await message.answer(hbold('👥Ваши чаты⬆️'), parse_mode=ParseMode.HTML, reply_markup=home_keyboard())


async def process_balance(message: types.Message):
    balance = hbold('👑У Вас премиум аккаунт💎')
    if not db.is_premium(message.from_user.id):
        hearts = db.get_user_hearts(message.from_user.id)
        balance = hbold(f'💳Баланс: {hearts}{strings.SYMBOL}')

    invitation = INVITE_LINK.format(message.from_user.id)
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('Пригласить', switch_inline_query=invitation))

    referrals = db.get_referrals(message.from_user.id)
    response = strings.balance_msg(balance, referrals, invitation)
    await message.answer(response, parse_mode=ParseMode.HTML, reply_markup=kb)


async def process_profile(message: types.Message):
    me = db.get_user(message.from_user.id)
    await message.answer(
        text(hbold('👤Мой профиль'), hitalic('Вы можете редактировать свои данные, выбирая нужные пункты ниже⬇️'),
             sep='\n'),
        parse_mode=ParseMode.HTML, reply_markup=home_keyboard())
    await display_user(message.from_user.id, me, markup=profile_edit_kb())
    await EditProfile.editing.set()
