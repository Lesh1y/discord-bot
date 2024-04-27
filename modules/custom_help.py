from typing import Optional

from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand


class NewHelp(DefaultHelpCommand):
    """Изменённая команда справки"""
    def __init__(self, **options):
        super().__init__()
        self.command_attrs = attrs = options.pop('command_attrs', {})
        attrs.setdefault('name', 'help')
        attrs.setdefault('help', 'Отобразить это сообщение')
        self.arguments_heading: str = options.pop('arguments_heading', 'Аргументы:')
        self.commands_heading: str = options.pop('commands_heading', 'Команды:')
        self.default_argument_description: str = options.pop('default_argument_description', 'Нет описания аргумента')
        self.no_category = options.pop('no_category', 'Без категории')

    def command_not_found(self, string: str, /) -> str:
        """Сообщение при отсутствии команды"""
        return f'Команда `.{string}` не найдена.'

    def get_ending_note(self):
        """Футер для подсказки"""
        command_name = self.invoked_with
        return f'Используйте {self.context.clean_prefix}{command_name} [команда] ' \
               'для получения информации о команде.\n' \
               f'Вы также можете использовать {self.context.clean_prefix}{command_name} [категория] ' \
               'для получения информации о категории.'

    async def command_callback(self, ctx: commands.Context, command: Optional[str] = None) -> None:
        """Отправка сообщения-подсказки"""
        await ctx.message.add_reaction('✅')
        await ctx.message.delete(delay=2)
        await super().command_callback(ctx, command=command)
