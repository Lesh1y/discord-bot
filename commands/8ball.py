"""Шар восьмёрка"""
from random import choice

from discord import Embed, Colour
from discord.ext import commands

from modules.conf import EIGHT_BALL_RESPONSES
from modules.logger import logger


class EightBall(commands.Cog, name='шар8'):
    """Обращение к восьмёрке"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.responses = EIGHT_BALL_RESPONSES

    @commands.command(name='8ball', aliases=('8b', 'шар', 'восьмёрка'))
    async def eight_ball(self, ctx: commands.Context, *, question):
        """
            Задайте вопрос восьмёрке (ツ)
            Ещё можно использовать .8ball, .8b, .шар, .восьмёрка
            Вызов команды: .шар Ты живой?
        """
        await ctx.message.add_reaction('✅')

        emb = Embed(title=':8ball: Шар восьмёрка :8ball:', colour=Colour.random())
        emb.add_field(name=':8ball: Вопрос:', value=f'{question}', inline=False)
        emb.add_field(name=':8ball: Ответ:', value=f'{choice(self.responses)}', inline=False)
        await ctx.send(embed=emb)
        await ctx.message.delete(delay=1)

    @eight_ball.error
    async def eight_ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.add_reaction('✅')
            await ctx.send('Вы пропустили аргумент команды! '
                           '\nПожалуйста, укажите вопрос. '
                           f'{ctx.author.mention}', delete_after=6)
            logger.info('Пропущен аргумент команды .8b')


async def setup(bot):
    """Настройка"""
    await bot.add_cog(EightBall(bot))
