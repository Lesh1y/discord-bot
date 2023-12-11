"""Выдача ролей по реакциям"""
from discord import RawReactionActionEvent, Member, Role
from discord.ext import commands
from discord.utils import get as get_dc_obj

from modules.conf import EnumOfPostIds, EnumOfRolesIds
from modules.logger import logger


class Roles(commands.Cog):
    """Роли по реакциям"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.post_id = EnumOfPostIds.roles_post.value
        self.roles = {
            '🎮': EnumOfRolesIds.gamer.value, '🧩': EnumOfRolesIds.it.value
        }

    def check_roles(self, payload: RawReactionActionEvent) -> None or tuple[Member, Role, bool]:
        emoji = str(payload.emoji)

        event_filter = any((
            payload.user_id == self.bot.user.id, payload.message_id != self.post_id,
            not self.roles.get(emoji)
        ))

        if event_filter:
            logger.info(
                'Событие добавления/снятия реакции проигнорировано, так как не соответствует фильтру'
            )
            return

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
            logger.info(f'{member} успешно получает роль "{role}"')
            return

        logger.info(f'{member} уже имеет роль "{role}"')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Событие 'удаление реакции / роли'"""
        if not (group := self.check_roles(payload)):
            return

        member, role, has_role = group

        if has_role:
            await member.remove_roles(role)
            logger.info(f'{member} успешно удалил роль "{role}')

        logger.info(f'{member} ещё не имеет роль "{role}"')


async def setup(bot: commands.Bot) -> None:
    """Настройка"""
    await bot.add_cog(Roles(bot))
