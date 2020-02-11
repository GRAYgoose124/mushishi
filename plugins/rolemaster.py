import json
from os import path
from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get


class Rolemaster(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.role_file = path.join(self.bot.resource_path, 'role_stats.json')
        self.role_data = {}
        try:
            with open(self.role_file, 'r') as f:
                self.role_data = json.load(f)
        except IOError:
            pass

    def __unload(self):
        with open(self.role_file, 'w') as f:
            json.dump(self.role_data, f)

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def addrole(self, ctx, *cmd):
        member = ctx.message.author
        role = get(member.server.roles, name=cmd[0])
        await self.bot.add_roles(member, role)


def setup(bot):
    bot.add_cog(Rolemaster(bot))
