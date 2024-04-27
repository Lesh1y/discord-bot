"""Пакет обработки событий"""
import logging
from datetime import datetime

from discord import Colour, Embed, File, Member
from discord.ext import commands

from modules.conf import bye_msg, hello_msg, MEMBER_ACTIONS


class EventsMixin(commands.Cog):
    """Группа обработки событий"""

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, err: commands.CommandError):
        """Обработчик неучтённых ошибок"""
        if any(
                (
                        ctx.command and ctx.command.has_error_handler(),
                        ctx.cog and ctx.cog.has_error_handler()
                )
        ):
            return

        await ctx.message.add_reaction('⚠️')
        await ctx.message.delete(delay=2)

        if isinstance(err, commands.CommandNotFound):
            await ctx.send(
                embed=Embed(
                    description=f'** {ctx.author.name}, данной команды не существует.**',
                    color=Colour.red()
                ),
                delete_after=2
            )

            logging.info(
                f'Пользователь {ctx.author.name} вызвал несуществующую команду {ctx.message.content}'
            )
            return

        logging.error(f'При выполнении команды {ctx.command} возникло исключение — {err}')

    @staticmethod
    async def message_sender_from_template(member: Member, action: str, random_value: str) -> None:
        """Формирование и отправка сообщения

        ----

        Note:

        Метод содержит в себе шаблон для сообщения, который заполняется на базе входных данных
        и отправляется в системный чат.

        ----
        :param member: Пользователь, подключившийся к серверу или отключившийся от него (:class:`discord.Member`).
        :param action: Событие — подключение или отключение пользователя (:class:`str`)
        :param random_value: Случайное значение для текста сообщения о событии (:class:`str`)
        """

        sys_channel = member.guild.system_channel
        data = MEMBER_ACTIONS

        # Уведомление о подключении
        file = File(data[action].img, filename=data[action].filename)
        embed = Embed(color=Colour.dark_green())
        embed.add_field(
            name=data[action].embed_name,
            value=data[action].text.format(random_value)
        )
        embed.set_image(url=f'attachment://{data[action].filename}')
        embed.set_footer(
            text=f'{datetime.now().strftime("%d-%m-%Y %H:%M")}'
                 f'\n{member.name} {data[action].ru_action}', icon_url=member.avatar.url
        )

        await sys_channel.send(embed=embed, file=file)
        logging.info(f'Пользователь {member.name} {data[action].ru_action}')

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        """При подключении пользователя к серверу (гильдии)"""
        await self.message_sender_from_template(member, 'join', hello_msg().format(member.mention))

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        """Обработчик отключения пользователя от сервера (гильдии)"""
        await self.message_sender_from_template(member, 'remove', bye_msg().format(member.name))


async def setup(bot: commands.Bot):
    """Функция для подключения группы команд к боту"""
    await bot.add_cog(EventsMixin())
