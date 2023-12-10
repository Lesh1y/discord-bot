from datetime import date
from logging import DEBUG
from os import getenv, getcwd
from os.path import join
from pathlib import Path


LOG_FILENAME = getenv('LOG_FILE_PATH', join(getcwd(), 'log', 'qwerty.log'))

# Uncomment needed log level:
# LOG_LEVEL = 50 # CRITICAL
# LOG_LEVEL = 40 # ERROR
# LOG_LEVEL = 30 # WARNING
# LOG_LEVEL = 20 # INFO
LOG_LVL = LOG_LEVEL = DEBUG


def hello_msg(member) -> tuple:
    hello_list = (
        f'{member.mention} залетел(а) на сервер!', f'Ура, {member.mention} теперь с нами!',
        f'{member.mention} приземляется на сервере.', f'{member.mention} присоединяется к вашей пати.',
        f'{member.mention} запрыгивает на сервере.', f'Дикий(ая) {member.mention} появился(ась).',
        f'Знакомьтесь, это {member.mention}!', f'{member.mention} уже здесь.',
        f'Рады тебя видеть, {member.mention}!', f'Привет, {member.mention}, поздоровайся со всеми!',
        f'Рады встрече, {member.mention}.', f'{member.mention} проскальзывает на сервере.'
    )
    return hello_list


def bye_msg(member) -> tuple:
    bye_list = (
        f'**{member.name}** улетел(а) с сервера!', f'Блин, **{member.name}** теперь не с нами!',
        f'**{member.name}** отправляется с сервера.', f'**{member.name}** отваливается от вашей пати.',
        f'**{member.name}** спрыгивает с сервера.', f'Дикий(ая) **{member.name}** исчез(ла).',
        f'Знакомьтесь, это **{member.name}** и он(а) свалил(а)!', f'**{member.name}** уже не здесь.',
        f'Мы будем скучать, **{member.name}**!', f'Пока, **{member.name}**, попрощайся со всеми!',
        f'До новой встречи, **{member.name}**.', f'**{member.name}** соскальзывает с сервера.', f'**{member.name}** '
                                                                                                f'ливает.'
    )
    return bye_list
