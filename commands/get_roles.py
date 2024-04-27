"""Выдача ролей по реакциям"""
import logging

from discord import RawReactionActionEvent, Member, Role
from discord.ext import commands
from discord.utils import get as get_dc_obj

from modules.conf import PostIds, RolesIds


class Roles(commands.Cog):
    """Роли по реакциям"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.post_id = PostIds.roles_post
        self.roles = {
            '🎮': RolesIds.gamer, '🧩': RolesIds.it
        }

    def check_roles(self, payload: RawReactionActionEvent) -> None or tuple[Member, Role, bool]:
        emoji = str(payload.emoji)

        event_filter = any((
            payload.user_id == self.bot.user.id, payload.message_id != self.post_id,
            not self.roles.get(emoji)
        ))

        if event_filter:
            logging.debug(
                'Событие добавления/снятия реакции проигнорировано, так как не соответствует фильтру'
            )
            return None

        guild = self.bot.get_guild(payload.guild_id)
        member = get_dc_obj(guild.members, id=payload.user_id) if not payload.member else payload.member
        role = get_dc_obj(guild.roles, id=self.roles[emoji])
        has_role = False

        if role in member.roles:
            has_role = True

        return member, role, has_role

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent) -> None:
        """Обработка события 'добавление реакции'"""
        if not (group := self.check_roles(payload)):
            return

        member, role, has_role = group

        if not has_role:
            await member.add_roles(role)
            logging.info(f'{member} успешно получает роль "{role}"')
            return

        logging.info(f'{member} уже имеет роль "{role}"')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Событие 'удаление реакции / роли'"""
        if not (group := self.check_roles(payload)):
            return

        member, role, has_role = group

        if has_role:
            await member.remove_roles(role)
            logging.info(f'{member} успешно удалил роль "{role}')

        logging.info(f'{member} ещё не имеет роль "{role}"')


async def setup(bot: commands.Bot):
    """Настройка"""
    await bot.add_cog(Roles(bot))

# TODO: Переосмыслить выдачу ролей. Добавить возможность для модераторов
#  динамически добавлять роли для выдачи по реакциям. Возможно, внедрить БД под это дело
