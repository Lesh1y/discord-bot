"""Пакет модерации"""
from datetime import datetime
from os import getenv
from typing import Union

import discord

from discord.ext import commands

from modules.logger import logger


class Moderation(commands.Cog, name='модерация'):
    """Команды для модераторов"""

    def __init__(self, bot):
        self.bot = bot

    def check_target_member_permissions(self, member: discord.Member, author_name: str) -> Union[int, str]:
        # Проверка на права бота у "цели"
        if member.id == self.bot.user.id:
            logger.info(f'модератор {author_name} попытался забанить бота')
            return ':no_entry: <@{}> Нельзя {} бота!\nОбратитесь к {}'

        # Проверка на наличие прав администратора/модератора у "цели"
        if any(
                (
                        member.guild_permissions.administrator,
                        member.guild_permissions.ban_members,
                        member.guild_permissions.kick_members
                )
        ):
            logger.info(f'модератор {author_name} попытался забанить администратора {member.display_name}')
            return ':no_entry: <@{}> Нельзя {} другого администратора/модератора, обратитесь к {}.'

        return 0

    @commands.has_permissions(ban_members=True)
    @commands.command(name='ban', aliases=['бан', 'забанить'])
    async def ban_user(
            self, ctx: commands.Context,
            user: discord.Member = commands.parameter(description='Пользователь, которого необходимо заблокировать.'),
            *, reason: str = commands.parameter(description='Причина блокировки.', default='Без причины')
    ):
        """
        Бан пользователя
        Для того, чтобы забанить пользователя, просто пинганите его после команды.
        Вы можете написать причину через пробел после пинга (необязательно).

        Пример команды: .ban @нарушитель спамит
        """
        await ctx.message.add_reaction('✅')
        await ctx.message.delete(delay=10)

        if not isinstance(resp := self.check_target_member_permissions(member=user, author_name=ctx.author.name), int):
            await ctx.send(
                resp.format(
                    ctx.author.id, 'заблокировать', getenv('GUILD_OWNER')
                ), delete_after=5
            )
            return

        # Бан
        await user.ban(reason=reason)

        # Уведомление о бане
        file = discord.File('img/ban.png', filename='ban.png')
        embed = discord.Embed(color=discord.Colour.red())
        embed.add_field(name='Бан пользователя!',
                        value=f'Пользователь {user.mention} был заблокирован.'
                              f'\nПричина: **{reason}**\nМодератор: {ctx.author.mention}')
        embed.set_image(url='attachment://ban.png')
        embed.set_footer(text=f'{datetime.now().strftime("%d-%m-%Y %H:%M")}'
                              f'\nВызвал(а) {ctx.author}', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed, file=file)
        logger.info(f'модератор {ctx.author} забанил {user.display_name}')

    @commands.has_permissions(kick_members=True)
    @commands.command(name='kick', aliases=['кик', 'кикнуть'])
    async def kick_user(
            self, ctx: commands.Context,
            user: discord.Member = commands.parameter(description='Пользователь, которого необходимо исключить.'),
            *, reason: str = commands.parameter(description='Причина исключения.', default='Без причины')
    ):
        """
        Кик пользователя
        Для того, чтобы кикнуть пользователя, просто пинганите его после команды.
        Вы можете написать причину через пробел после пинга (необязательно).

        Пример команды: .kick @нарушитель спамит
        """
        await ctx.message.add_reaction('✅')
        await ctx.message.delete(delay=10)

        if not isinstance(resp := self.check_target_member_permissions(member=user, author_name=ctx.author.name), int):
            await ctx.send(
                resp.format(
                    ctx.author.id, 'исключить', getenv('GUILD_OWNER')
                ), delete_after=5
            )
            return

        # Кик
        await user.kick(reason=reason)

        # Уведомление о кике
        file = discord.File('img/kick.png', filename='kick.png')
        embed = discord.Embed(color=discord.Colour.red())
        embed.add_field(name='Исключение пользователя!',
                        value=f'Пользователь {user.mention} был исключён.'
                              f'\nПричина: **{reason}**\nМодератор: {ctx.author.mention}')
        embed.set_image(url='attachment://kick.png')
        embed.set_footer(text=f'{datetime.now().strftime("%d-%m-%Y %H:%M")}'
                              f'\nВызвал(а) {ctx.author}', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed, file=file)

        logger.info(f'модератор {ctx.author} кикнул {user.display_name}')

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['c', 'cl', 'чистка', 'удалить'])
    async def clear(
            self, ctx: commands.Context,
            amount: int = commands.parameter(description='Количество сообщений для удаления', default=1)
    ):
        """
        Очистка чата от сообщений
        Напишите команду и количество сообщений, которое хотите удалить.
        Например, .clear 5
        Команду можно вызвать, не указывая количество сообщений для удаления.
        В таком случае будет удалено одно сообщение.

        !Команда удаляется автоматически и не требует учёта!
        """
        await ctx.message.add_reaction('✅')
        await ctx.channel.purge(limit=amount + 1)

    @commands.has_permissions(ban_members=True)
    @commands.command(name='unban', aliases=['анбан', 'разбан', 'разбанить'])
    async def unban_user(
            self, ctx: commands.Context,
            user: str = commands.parameter(description='Никнейм пользователя для разблокировки'),
    ):
        """
        Разблокировка пользователя
        Для того, чтобы разблокировать пользователя, просто напишите его ник после команды.

        Пример команды: .unban нарушитель777
        """
        await ctx.message.add_reaction('✅')
        await ctx.message.delete(delay=5)

        # разбан
        async for banned in ctx.guild.bans():
            if banned.user.name == user:
                await ctx.guild.unban(banned.user)

                # Уведомление о разбане
                file = discord.File('img/unban.png', filename='unban.png')
                embed = discord.Embed(color=discord.Colour.green())
                embed.add_field(name='Разблокировка пользователя!',
                                value=f'Пользователь {banned.user.mention} был разблокирован.'
                                      f'\nМодератор: {ctx.author.mention}')
                embed.set_image(url='attachment://unban.png')
                embed.set_footer(text=f'{datetime.now().strftime("%d-%m-%Y %H:%M")}'
                                      f'\nВызвал(а) {ctx.author}', icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed, file=file)
                logger.info(f'модератор {ctx.author} разбанил {banned.user.display_name}')
                return

        await ctx.send(f':no_entry: Пользователь `{user}` не найден в списке заблокированных', delete_after=4)

    @commands.has_permissions(kick_members=True)
    @commands.command(name='warn', aliases=['предупредить', 'предупреждение'])
    async def warn_user(
            self, ctx: commands.Context,
            user: discord.Member = commands.parameter(description='Пользователь, которого необходимо предупредить.'),
            *, reason: str = commands.parameter(description='Причина предупреждения.', default='Без причины')
    ):
        """
        Предупреждение пользователя
        Для того, чтобы предупредить пользователя, просто пинганите его после команды.
        Вы можете написать причину через пробел после пинга (необязательно).

        Пример команды: .warn @нарушитель777 спамит
        """
        await ctx.message.add_reaction('✅')
        await ctx.message.delete(delay=5)

        # Предупреждение
        # TODO: подготовить изображение для предупреждения пользователя или подумать об его отсутствии
        # file = discord.File('img/warn.png', filename='warn.png')
        embed = discord.Embed(color=discord.Colour.gold())
        embed.add_field(name='Предупреждение пользователя!',
                        value=f'Пользователь {user.mention} был предупрежён.'
                              f'\nПричина: **{reason}**\nМодератор: {ctx.author.mention}')
        # embed.set_image(url='attachment://warn.png')
        embed.set_footer(text=f'{datetime.now().strftime("%d-%m-%Y %H:%M")}'
                              f'\nВызвал(а) {ctx.author}', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)  # , file=file)
        logger.info(f'модератор {ctx.author} предупредил {user.display_name}')

    @commands.has_permissions(kick_members=True)
    @commands.command(name='info', aliases=['inf', 'инфа'])
    async def user_info(
            self, ctx: commands.Context,
            user: discord.Member = commands.parameter(
                description='Пользователь, информацию о котором необходимо вывести.'
            )
    ):

        """Информация о пользователе"""
        await ctx.message.add_reaction('✅')
        await ctx.message.delete(delay=5)

        embed = discord.Embed(color=user.color)
        embed.add_field(
            name='Информация о пользователе!',
            value=f'Пользователь {user.mention} зашёл на сервер {user.joined_at.strftime("%d.%m.%Y %I:%M %p")}.'
                  f'\nЛогин пользователя: `{user.name}`'
                  f'\nСписок ролей пользователя: `{", ".join([role.name for role in user.roles])}`'
        )
        embed.set_footer(text=f'{datetime.now().strftime("%d-%m-%Y %H:%M")}'
                              f'\nВызвал(а) {ctx.author}', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        logger.info(f'модератор {ctx.author} отобразил информацию о пользователе {user.display_name}')

    @ban_user.error
    @kick_user.error
    @warn_user.error
    async def ban_kick_and_warn_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.add_reaction('✅')
            await ctx.send(f'Вы пропустили аргумент команды `.{ctx.command}`! '
                           '\nПожалуйста, укажите пользователя с помощью пинга. '
                           f'{ctx.author.mention}', delete_after=6)
            logger.info(f'Пропущен аргумент команды .{ctx.command}')
            await ctx.message.delete(delay=1)

        elif isinstance(error, commands.BadArgument):
            await ctx.message.add_reaction('✅')
            await ctx.send(f'Вы использовали неверный аргумент команды `.{ctx.command}`! '
                           '\nПожалуйста, укажите пользователя с помощью пинга. '
                           'И убедитесь, что он присутствует на сервере'
                           f'{ctx.author.mention}', delete_after=6)
            logger.info(f'Неверно введён аргумент команды .{ctx.command}')
            await ctx.message.delete(delay=1)

        elif isinstance(error, commands.MissingPermissions):

            await ctx.message.add_reaction('✅')
            await ctx.send(':no_entry: У вас нет прав на использование команды `.{ctx.command}`! '
                           f'{ctx.author.mention}', delete_after=6)
            logger.info(f'У {ctx.author} недостаточно прав для использования команды .{ctx.command}')
            await ctx.message.delete(delay=1)

    @clear.error
    async def clear_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.add_reaction('❌')
            await ctx.send(':no_entry: У вас нет прав на использование данной команды! '
                           f'{ctx.author.mention}', delete_after=6)
            logger.info(f'У {ctx.author} недостаточно прав для использования команды .clear')
            await ctx.message.delete(delay=1)

    @unban_user.error
    async def unban_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.add_reaction('✅')
            await ctx.send('Вы пропустили аргумент команды! '
                           '\nПожалуйста, укажите ник пользователя. '
                           f'{ctx.author.mention}', delete_after=6)
            logger.info('Пропущен аргумент команды .unban')
            await ctx.message.delete(delay=1)

        elif isinstance(error, commands.BadArgument):
            await ctx.message.add_reaction('✅')
            await ctx.send('Вы использовали неверный аргумент команды! '
                           '\nПожалуйста, укажите ник пользователя. '
                           f'{ctx.author.mention}', delete_after=6)
            logger.info('Неверно введён аргумент команды .unban')
            await ctx.message.delete(delay=1)

        elif isinstance(error, commands.MissingPermissions):
            await ctx.message.add_reaction('❌')
            await ctx.send(':no_entry: У вас нет прав на использование данной команды! '
                           f'{ctx.author.mention}', delete_after=6)
            logger.info(f'У {ctx.author} недостаточно прав для использования команды .unban')
            await ctx.message.delete(delay=1)


async def setup(bot):
    """Настройка"""
    await bot.add_cog(Moderation(bot))
