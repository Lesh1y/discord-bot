import logging

from os import getenv
from pathlib import Path
from typing import NoReturn

from discord import Intents, Activity, ActivityType
from discord.ext import commands
from dotenv import load_dotenv

from modules.custom_help import NewHelp


class QwertyBot(commands.Bot):
    _instance: 'QwertyBot' = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        """Многофункциональный самописный бот для Discord"""
        super().__init__(
            command_prefix=self.prefix, intents=self.get_intents, case_insensitive=True,
            help_command=NewHelp()
        )

        self._cogs = [p.stem for p in Path('.').glob('commands/*.py')]

    async def on_ready(self) -> None:
        """Обработка события `при готовности`"""
        # настройка "активности" (дополнительная подсказка для пользователя в профиле бота)
        await self.change_presence(
            activity=Activity(
                type=ActivityType.listening,
                name='.help'))

        # настройка групп команд
        for cog in self._cogs:
            logging.debug(f'Начата загрузка группы команд {cog} ...')

            try:
                await self.load_extension(f'commands.{cog}')
            except commands.ExtensionAlreadyLoaded:
                logging.warning(f'Группа команд {cog} была загружена ранее, пропускаю ...')
            except commands.ExtensionNotFound:
                logging.warning(f'Группа команд {cog} не найдена, пропускаю ...')
            else:
                logging.info(f'Группа команд {cog} успешно загружена!')

        logging.info('Бот запущен!')

    @property
    def get_intents(self) -> Intents:
        """Метод, формирующий `Намерения` (позволяет расширить функционал и обрабатываемые фичи)"""
        return Intents.all()

    @staticmethod
    def prefix(bot, msg) -> list[str]:
        """Метод, формирующий префикс для команд бота"""
        return commands.when_mentioned_or('.')(bot, msg)

    def startup(self) -> NoReturn:
        """Метод, запускающий бота"""
        load_dotenv()
        token = getenv('TOKEN')

        self.run(token)
