"""Модуль, содержащий код для обработки команд, связанных с шаром-восьмёркой"""
import logging

from discord import Embed, Colour
from discord.ext import commands

from modules.conf import eight_ball_answer


class EightBall(commands.Cog, name='Шар-восьмёрка'):
    """Набор команд и обработчиков для шара-восьмёрки"""

    @commands.command(name='8ball', aliases=('8b', 'шар', 'восьмёрка'))
    async def eight_ball(
            self, ctx: commands.Context,
            *, question: str = commands.parameter(description='Вопрос для шара.')
    ):
        """Шар-Восьмёрка
            Задайте вопрос восьмёрке (ツ)
            Ещё можно использовать .8ball, .8b, .шар, .восьмёрка
            Вызов команды: .шар Ты живой?
        """
        logging.debug(f'{ctx.author.name} вызвал команду .8ball')

        await ctx.message.add_reaction('✅')
        await ctx.message.delete(delay=2)

        embed = Embed(title=':8ball: Шар восьмёрка :8ball:', colour=Colour.random())
        embed.add_field(name=':question: Вопрос:', value=f'{question}', inline=False)
        embed.add_field(name=':8ball: Ответ:', value=f'{eight_ball_answer()}', inline=False)

        await ctx.send(embed=embed)

    @eight_ball.error
    async def eight_ball_error(self, ctx: commands.Context, error: commands.CommandError):
        """Обработка ошибок, связанных с набором 'Шар-Восьмёрка'"""
        if isinstance(error, commands.MissingRequiredArgument):
            logging.info(f'{ctx.author.name} пропустил аргумент команды .8ball')

            await ctx.message.add_reaction('⚠️')
            await ctx.message.delete(delay=2)

            await ctx.send(
                'Вы пропустили аргумент команды!\nПожалуйста, укажите вопрос, '
                f'{ctx.author.mention}', delete_after=6
            )


async def setup(bot: commands.Bot):
    """Функция для подключения группы команд к боту"""
    await bot.add_cog(EightBall())
