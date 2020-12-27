import json
from os import path
from discord.ext import commands, tasks
from discord.ext.commands import Cog
from discord.utils import get


class Rolemaster(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.role_file = path.join(self.bot.resource_path, 'data/role_stats.json')
        self.role_data = {}

        try:
            with open(self.role_file, 'r') as f:
                self.role_data = json.load(f)
        except (IOError, ValueError):
            with open(self.role_file, 'w') as f:
                json.dump(self.role_data, f)

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def addrole(self, ctx, *cmd):
        member = ctx.message.author
        role = get(member.server.roles, name=cmd[0])
        await self.bot.add_roles(member, role)

    @commands.Cog.listener()
    async def on_message(self, m):
        if m.author.name not in self.role_data:
            self.role_data[m.author.name] = {}
            self.role_data[m.author.name]['xp'] = 0
            self.role_data[m.author.name]['level'] = 1
            self.role_data[m.author.name]['xp_needed'] = 2 ** self.role_data[m.author.name]['level'] + 200
        else:
            self.role_data[m.author.name]['xp'] += len(set(m.content))
            if self.role_data[m.author.name]['xp'] >= self.role_data[m.author.name]['xp_needed']:



                if not m.author.bot and not m.author.server_permissions.administrator:
                    await self.bot.remove_roles(m.author, m.server.roles[self.role_data[m.author.name]['level']] - 1)

                self.role_data[m.author.name]['level'] += 1
                self.role_data[m.author.name]['xp_needed'] = 2 ** self.role_data[m.author.name]['level']
                await m.channel.send(f"Congrats {m.author.name}, you're now level {self.role_data[m.author.name]['level']}.")

                if not m.author.bot and not m.author.server_permissions.administrator:
                    await self.bot.add_roles(m.author, m.server.roles[self.role_data[m.author.name]['level']])
                await m.channel.send(f"Your new role is {m.server.roles[self.role_data[m.author.name]['level']]}.")

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def rolestats(self, m, *cmd):
        await m.channel.send(f"You're level {self.role_data[m.author.name]['level']} with {self.role_data[m.author.name]['xp']}/{self.role_data[m.author.name]['xp_needed']}.")


def setup(bot):
    bot.add_cog(Rolemaster(bot))


def teardown(bot):
    print("got here")
    # with open(bot.role_file, 'w') as f:
    #     print("RM: Saving role stats.")
    #     json.dump(bot.role_data, f)
    #     print("RM: Done.")
    print("gotem")