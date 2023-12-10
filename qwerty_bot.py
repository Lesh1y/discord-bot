from datetime import datetime
from os import getenv
from pathlib import Path
from random import choice
from typing import NoReturn

from discord import Activity, ActivityType, Colour, Embed, File, Intents, Member
from discord.ext import commands
from dotenv import load_dotenv

from modules.conf import bye_msg, Channels, hello_msg
from modules.logger import logger


class QwertyBot(commands.Bot):
    def __init__(self):
        """Многофункциональный самописный бот для Discord"""
        self._cogs = [p.stem for p in Path(".").glob("commands/*.py")]
        super().__init__(
            command_prefix=self.prefix, intents=self.get_intents, case_insensitive=True
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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        """Обработчик ошибок"""
        await ctx.message.add_reaction('✅')
        logger.info(err)

        if isinstance(err, commands.CommandNotFound):
            await ctx.send(embed=Embed(
                description=f'** {ctx.author.name}, данной команды не существует.**',
                color=Colour.red()), delete_after=2)
        await ctx.message.delete(delay=1)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """При подключении пользователя"""
        channel = member.guild.system_channel

        # Уведомление о подключении
        file = File('img/join.png', filename='join.png')
        embed = Embed(color=Colour.dark_green())
        embed.add_field(name='Добро пожаловать!',
                        value=f'{choice(hello_msg(member))}'
                              f'\n**Рады тебя видеть!** \n Загляни в {Channels.rules} (ツ) '
                              f'И не забудь подобрать себе роль по вкусу в {Channels.roles} '
                              ':stuck_out_tongue_winking_eye: ')
        embed.set_image(url='attachment://join.png')
        embed.set_footer(text=f'{datetime.now().strftime("%d-%m-%Y %H:%M")}'
                              f'\n{member.name} присоединился', icon_url=member.avatar.url)
        await channel.send(embed=embed, file=file)
        logger.info(f'пользователь {member.name} подключился к серверу')

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        """При отключении пользователя"""
        channel = member.guild.system_channel

        # Уведомление об отключении
        file = File('img/leave.gif', filename='leave.gif')
        embed = Embed(color=Colour.dark_green())
        embed.add_field(name='До новых встреч!',
                        value=f'{choice(bye_msg(member))}'
                              '\n**Жаль, что ты уходишь!** \n Надеемся на твоё скорейшее возвращение (ツ)')
        embed.set_image(url='attachment://leave.gif')
        embed.set_footer(text=f'{datetime.now().strftime("%d-%m-%Y %H:%M")}'
                              f'\n{member.name} ливнул(а)', icon_url=member.avatar.url)
        await channel.send(embed=embed, file=file)
        logger.info(f'пользователь {member.name} покинул сервер')

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
