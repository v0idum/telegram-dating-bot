from aiogram.utils.markdown import *

SYMBOL = '💘'

MALE = '👦🏻Парень'
FEMALE = '👩🏼Девушка'

#  Search Gender
MALE_SEARCH = '👦🏻Парня'
FEMALE_SEARCH = '👩🏼Девушку'

NEXT = 'next'
BACK = 'Вернуться'

SEARCH = '🔎Поиск'
CONVERSE = '💬Общение'
PROFILE = '👤Профиль'
BALANCE = f'{SYMBOL}️Баланс'

LIKE = 'like'
CHAT = 'chat'
MORE = 'profile'

# Age majority confirmation
YES = 'Да'
NO = 'Нет'


def welcome_msg():
    return text(hbold(f'Приветствую❗Меня зовут Купидон, Я - Бог Любви!{SYMBOL}'),
                hbold('И раз Вы обратились ко мне, считайте, что вторая половинка для Вас уже найдена!😉'),
                hbold('Давайте быстренько заполним анкету и приступим к поиску Вашей любви!💞'),
                sep='\n')


def balance_msg(balance, referrals, invitation):
    return text(balance, '\n',
                hitalic(f'  1{SYMBOL} = Свайп при поиске собеседника'),
                hitalic(f'  5{SYMBOL} = Лайкнуть пользователя'),
                hitalic(f'10{SYMBOL} = Каждое сообщение пользователю, который Вам ещё не ответил'),
                hitalic(f'  5{SYMBOL} = Просмотр профиля того, кто лайкнул Вас или написал Вам'),
                '\n',
                hbold(f'Вы можете зарабатывать сердечки{SYMBOL}, приглашая в бот своих друзей и знакомых👨‍👦‍👦'),
                '\n',
                hitalic(f'10{SYMBOL} за приглашение парня'),
                hitalic(f'50{SYMBOL} за приглашение девушки'),
                '\n',
                hcode(f'Уже приглашено: {referrals}'),
                '\n',
                hbold('Ваша уникальная ссылка для приглашения в бот:'),
                text(invitation),
                sep='\n')


def user_info(user):
    return text(text(hcode('Имя:'), hbold(user[1])), text(hcode('Возраст:'), hbold(user[2])),
                text(hcode('Город:'), hbold(user[3])), text(hcode('Род занятий:'), hbold(user[4])),
                text(hcode('О себе:'), hbold(user[5])),
                sep='\n')
