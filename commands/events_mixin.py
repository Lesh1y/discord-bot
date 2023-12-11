from datetime import datetime
from random import choice

from discord import Colour, Embed, File, Member
from discord.ext import commands
from modules.conf import bye_msg, EnumOfChannelsMentions, hello_msg
from modules.logger import logger


class EventsMixin(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, err: commands.CommandError):
        """Обработчик ошибок"""
        await ctx.message.add_reaction('✅')
        if isinstance(err, commands.CommandNotFound):
            await ctx.send(embed=Embed(
                description=f'** {ctx.author.name}, данной команды не существует.**',
                color=Colour.red()), delete_after=2)

            logger.info(
                f'Пользователь {ctx.author.name} вызвал несуществующую команду {ctx.message.content}\n{err=}'
            )

        await ctx.message.delete(delay=1)

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        """При подключении пользователя"""
        channel = member.guild.system_channel

        # Уведомление о подключении
        file = File('img/join.png', filename='join.png')
        embed = Embed(color=Colour.dark_green())
        embed.add_field(name='Добро пожаловать!',
                        value=f'{choice(hello_msg(member))}'
                              f'\n**Рады тебя видеть!** \n Загляни в {EnumOfChannelsMentions.rules.value} (ツ) '
                              f'И не забудь подобрать себе роль по вкусу в {EnumOfChannelsMentions.roles.value} '
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


async def setup(bot: commands.Bot) -> None:
    """Настройка"""
    await bot.add_cog(EventsMixin())
