from os import getenv
from pathlib import Path
from typing import NoReturn

from discord import Intents, Activity, ActivityType
from discord.ext import commands
from dotenv import load_dotenv

from modules.logger import logger
from modules.custom_help import NewHelp


class QwertyBot(commands.Bot):
    def __init__(self):
        """Многофункциональный самописный бот для Discord"""
        self._cogs = [p.stem for p in Path(".").glob("commands/*.py")]
        super().__init__(
            command_prefix=self.prefix, intents=self.get_intents, case_insensitive=True,
            help_command=NewHelp()
        )

    async def on_ready(self) -> None:
        """Обработка события `при готовности`"""
        # настройка "активности" (дополнительная подсказка для пользователя на иконке бота)
        await self.change_presence(
            activity=Activity(
                type=ActivityType.listening,
                name='.help'))

        # настройка команд
        try:
            for cog in self._cogs:
                await self.load_extension(f'commands.{cog}')
                logger.info(f'[загрузка] {cog}')
        except Exception as e:
            logger.error(e)

    @property
    def get_intents(self) -> Intents:
        """Метод, формирующий `Намерения` (позволяет расширить функционал и обрабатываемые фичи)"""
        intents = Intents.all()
        return intents

    @staticmethod
    async def prefix(bot, msg) -> list[str]:
        """Метод, формирующий префикс для команд бота"""
        return commands.when_mentioned_or('.')(bot, msg)

    def startup(self) -> NoReturn:
        """Метод, запускающий бота"""
        load_dotenv()
        token = getenv('TOKEN')
        self.run(token)
