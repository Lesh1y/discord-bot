from collections import namedtuple
from dataclasses import dataclass
from logging import DEBUG, INFO
from os import getenv, getcwd
from os.path import join
from random import choice

from discord.ext import commands

BYE_MESSAGES = (
        '**{}** улетел(а) с сервера!', 'Блин, **{}** теперь не с нами!',
        '**{}** отправляется с сервера.', '**{}** отваливается от вашей пати.',
        '**{}** спрыгивает с сервера.', 'Дикий(ая) **{}** исчез(ла).',
        'Знакомьтесь, это **{}** и он(а) свалил(а)!', '**{}** уже не здесь.',
        'Мы будем скучать, **{}**!', 'Пока, **{}**, попрощайся со всеми!',
        'До новой встречи, **{}**.', '**{}** соскальзывает с сервера.',
        '**{}** ливает.'
    )

EIGHT_BALL_RESPONSES = (
        'Бесспорно', 'Предрешено', 'Никаких сомнений', 'Определённо да',
        'Можешь быть уверен в этом', 'Мне кажется — «да»', 'Вероятнее всего',
        'Хорошие перспективы', 'Знаки говорят — «да»', 'Да', 'Пока не ясно, попробуй снова',
        'Спроси позже', 'Лучше не рассказывать', 'Сейчас нельзя предсказать',
        'Сконцентрируйся и спроси опять', 'Даже не думай', 'Мой ответ — «нет»',
        'По моим данным — «нет»', 'Перспективы не очень хорошие', 'Весьма сомнительно',
    )

HELLO_MESSAGES = (
        '{} залетел(а) на сервер!', 'Ура, {} теперь с нами!',
        '{} приземляется на сервере.', '{} присоединяется к вашей пати.',
        '{} запрыгивает на сервере.', 'Дикий(ая) {} появился(ась).',
        'Знакомьтесь, это {}!', '{} уже здесь.',
        'Рады тебя видеть, {}!', 'Привет, {}, поздоровайся со всеми!',
        'Рады встрече, {}.', '{} проскальзывает на сервере.'
    )


def bye_msg() -> str:
    """Функция создания прощального сообщения

    Returns:
        str: Прощальное сообщение.
    """

    return choice(BYE_MESSAGES)


def eight_ball_answer():
    """Функция создания ответа восьмёрки

    Returns:
        str: Ответ восьмёрки.
    """

    return choice(EIGHT_BALL_RESPONSES)


@dataclass
class ChannelsMentions:
    rules = getenv('RULES_CHAT_MENTION', '<#539833779095601152>')
    roles = getenv('ROLES_CHAT_MENTION', '<#747843889725177917>')


@dataclass
class PostIds:
    roles_post = getenv('ROLES_POST_ID', 747846534497828925)


@dataclass
class RolesIds:
    gamer = getenv('GAMER_ROLE_ID', 747471674374488105)
    it = getenv('IT_ROLE_ID', 739003525396168796)


def hello_msg() -> str:
    """Функция создания приветственного сообщения

    Returns:
        str: Приветственное сообщение.
    """

    return choice(HELLO_MESSAGES)


ON_MEMBER_ACTION_NT = namedtuple('MemberAction', 'img filename embed_name text ru_action')

MEMBER_ACTIONS = {
    'join': ON_MEMBER_ACTION_NT(
        'img/join.png', 'join.png', 'Добро пожаловать!',
        '{}\n**Рады тебя видеть!**\n'
        f'Загляни в {ChannelsMentions.rules} (ツ)'
        f'\nИ не забудь подобрать себе роль по вкусу в {ChannelsMentions.roles} '
        ':stuck_out_tongue_winking_eye:',
        'присоединился(ась)'
    ),
    'remove': ON_MEMBER_ACTION_NT(
        'img/leave.gif', 'leave.gif', 'До новых встреч!',
        '{}\n**Жаль, что ты уходишь!** \n Надеемся на твоё скорейшее возвращение (ツ)',
        'отключился(ась)'
    )
}

MODERATION_ERROR_ANSWER = namedtuple('ErrorAnswer', 'emoji text log_msg')

MODERATION_COG_ERRORS = {
    commands.errors.MissingRequiredArgument: MODERATION_ERROR_ANSWER(
        '⚠️',
        'Вы пропустили аргумент команды `.{}`! Введите `.help {}` для получения информации о команде.',
        'Пользователь {} пропустил аргумент команды .{}'
    ),
    commands.errors.BadArgument: MODERATION_ERROR_ANSWER(
        '⚠️',
        'Вы использовали неверный аргумент команды `.{}`! Введите `.help {}` для получения информации о команде.',
        'Пользователь {} неверно ввёл аргумент команды .{}'
    ),
    commands.errors.MissingPermissions: MODERATION_ERROR_ANSWER(
        '❌',
        ':no_entry: У вас нет прав на использование команды `.{}`! Обратитесь к администратору.',
        'У {} недостаточно прав для использования команды .{}'
    ),
}

LOGS_DIR = getenv('LOGS_DIR', join(getcwd(), 'logs'))
LOG_FILE_PATH = getenv('LOG_FILE_PATH', join(LOGS_DIR, 'qwerty.log'))

LOG_FILE_LEVEL = INFO
LOG_STREAM_LEVEL = DEBUG

# TODO: подумать над переработкой конфигурационного файла. Возможно, имеет смысл разделить по группам
