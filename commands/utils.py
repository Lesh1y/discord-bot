"""Какие-то утилиты"""
from discord.ext import commands


class Utils(commands.Cog, name='Утилиты'):
    """Утилиты"""

    @commands.command(aliases=('p',))
    async def ping(self, ctx) -> None:
        """Команда возвращает 'pong' в чат"""
        await ctx.message.add_reaction('✅')

        await ctx.send('pong', delete_after=1)

        await ctx.message.delete(delay=1)


async def setup(bot: commands.Bot):
    """Функция для подключения группы команд к боту"""
    await bot.add_cog(Utils())
