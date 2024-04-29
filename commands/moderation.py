"""Пакет модерации"""
import logging
from datetime import datetime
from os import getenv
from typing import Union

import discord

from discord.ext import commands

from modules.conf import MODERATION_COG_ERRORS


class Moderation(commands.Cog, name='Модерация'):
    """Набор команд для модераторов"""

    @staticmethod
    def check_target_member_permissions(
            context: commands.Context,
            action: str,
            member: discord.Member,
    ) -> Union[int, str]:
        """**Метод фильтрации действий по правам "цели".**

        ----

        Note:

        Здесь мы проверяем, не пытается ли пользователь забанить бота или другого администратора/модератора.

        ----

        :param context: Контекст вызова команды (:class:`commands.Context`).
        :param action: Действие [заблокировать | выгнать] над пользователем,
            доступность которого необходимо проверить (:class:`str`).
        :param member: Пользователь, над котором производится попытка выполнить действие (:class:`discord.Member`).
        """
        owner = getenv("GUILD_OWNER")

        # Проверка на права бота у "цели"
        if member.id == context.bot.user.id:
            logging.info(f'модератор {context.author.name} попытался забанить бота')
            return f':no_entry: {context.author.mention}, нельзя {action} бота!'

        # Проверка на наличие прав администратора/модератора у "цели"
        if any(
                (
                        member.guild_permissions.administrator,
                        member.guild_permissions.ban_members,
                        member.guild_permissions.kick_members
                )
        ):
            logging.info(
                f'{context.author.name} попытался забанить другого модератора/администратора {member.display_name}'
            )
            return (
                f':no_entry: {context.author.mention} Нельзя {action} другого администратора/модератора, '
                f'обратитесь к {owner}.'
            )

        return 0

    @commands.has_permissions(ban_members=True)
    @commands.command(name='ban', aliases=['бан', 'забанить'])
    async def ban_user(
            self, ctx: commands.Context,
            user: discord.Member = commands.parameter(description='Пользователь, которого необходимо заблокировать.'),
            *, reason: str = commands.parameter(description='Причина блокировки.', default='Без причины')
    ):
        """
        Бан пользователя.

        Для того чтобы забанить пользователя, просто пинганите его после команды.
        Вы можете написать причину через пробел после пинга (необязательно).

        Пример команды: .ban @нарушитель спамит
        """
        await ctx.message.delete(delay=5)

        if not isinstance(
                resp := self.check_target_member_permissions(action='заблокировать', context=ctx, member=user), int
        ):
            await ctx.message.add_reaction('❌')
            await ctx.send(resp, delete_after=5)

            return

        await ctx.message.add_reaction('✅')

        await user.ban(reason=reason)

        file = discord.File('img/ban.png', filename='ban.png')
        embed = discord.Embed(color=discord.Colour.red())
        embed.add_field(name='Бан пользователя!',
                        value=f'Пользователь {user.mention} был заблокирован.'
                              f'\nПричина: **{reason}**\nМодератор: {ctx.author.mention}')
        embed.set_image(url='attachment://ban.png')
        embed.set_footer(text=f'{datetime.now().strftime("%d-%m-%Y %H:%M")}'
                              f'\nВызвал(а) {ctx.author}', icon_url=ctx.author.avatar.url)

        await ctx.send(embed=embed, file=file)

        logging.info(f'модератор {ctx.author} заблокировал {user.display_name}')

    @commands.has_permissions(kick_members=True)
    @commands.command(name='kick', aliases=['кик', 'кикнуть'])
    async def kick_user(
            self, ctx: commands.Context,
            user: discord.Member = commands.parameter(description='Пользователь, которого необходимо исключить.'),
            *, reason: str = commands.parameter(description='Причина исключения.', default='Без причины')
    ):
        """
        Кик пользователя.

        Для того чтобы кикнуть пользователя, просто пинганите его после команды.
        Вы можете написать причину через пробел после пинга (необязательно).

        Пример команды: .kick @нарушитель спамит
        """
        await ctx.message.add_reaction('✅')
        await ctx.message.delete(delay=5)

        if not isinstance(
                resp := self.check_target_member_permissions(action='выгнать', context=ctx, member=user), int
        ):
            await ctx.send(
                resp.format(
                    ctx.author.id, 'исключить', getenv('GUILD_OWNER')
                ), delete_after=5
            )
            return

        await user.kick(reason=reason)

        file = discord.File('img/kick.png', filename='kick.png')
        embed = discord.Embed(color=discord.Colour.red())
        embed.add_field(name='Исключение пользователя!',
                        value=f'Пользователь {user.mention} был исключён.'
                              f'\nПричина: **{reason}**\nМодератор: {ctx.author.mention}')
        embed.set_image(url='attachment://kick.png')
        embed.set_footer(text=f'{datetime.now().strftime("%d-%m-%Y %H:%M")}'
                              f'\nВызвал(а) {ctx.author}', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed, file=file)

        logging.info(f'модератор {ctx.author} кикнул {user.display_name}')

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['c', 'cl', 'чистка', 'удалить'])
    async def clear(
            self, ctx: commands.Context,
            amount: int = commands.parameter(description='Количество сообщений для удаления', default=1)
    ):
        """
        Очистка чата от сообщений.

        Напишите команду и количество сообщений, которое хотите удалить.

        Например, .clear 5

        Команду можно вызвать, не указывая количество сообщений для удаления.
        В таком случае будет удалено одно сообщение.

        ! Команда удаляется автоматически и не требует учёта !
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

        async for banned in ctx.guild.bans():
            if banned.user.name == user:
                await ctx.guild.unban(banned.user)

                file = discord.File('img/unban.png', filename='unban.png')
                embed = discord.Embed(color=discord.Colour.green())
                embed.add_field(name='Разблокировка пользователя!',
                                value=f'Пользователь {banned.user.mention} был разблокирован.'
                                      f'\nМодератор: {ctx.author.mention}')
                embed.set_image(url='attachment://unban.png')
                embed.set_footer(text=f'{datetime.now().strftime("%d-%m-%Y %H:%M")}'
                                      f'\nВызвал(а) {ctx.author}', icon_url=ctx.author.avatar.url)

                await ctx.send(embed=embed, file=file)
                logging.info(f'модератор {ctx.author} разбанил {banned.user.display_name}')
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
        logging.info(f'модератор {ctx.author} предупредил {user.display_name}')

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
        logging.info(f'модератор {ctx.author} отобразил информацию о пользователе {user.display_name}')

    async def cog_command_error(self, ctx: commands.Context, error: Exception):
        """Обработчик исключений, связанных с командами модерации"""
        await ctx.message.delete(delay=2)

        try:
            emoji, answer, log_msg = MODERATION_COG_ERRORS.get(type(error))
        except TypeError:
            await ctx.message.add_reaction('🤔')
            await ctx.send(
                f'При выполнении команды `.{ctx.command}` возникло неизвестное исключение!\n'
                f'Обратитесь к {ctx.guild.owner.mention}', delete_after=6)
            logging.error(
                f'При выполнении команды `.{ctx.command}` возникло неизвестное исключение: {error} — {type(error)}'
            )
            return

        await ctx.message.add_reaction(emoji)

        await ctx.send(
            f'{answer.format(ctx.command, ctx.command)}\n{ctx.author.mention}',
            delete_after=6
        )

        logging.info(log_msg.format(ctx.author.name, ctx.command))


async def setup(bot: commands.Bot):
    """Функция для подключения группы команд к боту"""
    await bot.add_cog(Moderation())
