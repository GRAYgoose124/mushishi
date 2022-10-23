# Mushishi: A smart discord bot using the discord.py[rewrite] API.
# Copyright (C) 2018  Grayson Miller
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from discord.ext import commands
from discord.errors import NotFound, Forbidden
from discord.ext.commands import Cog
from discord import DMChannel
from traceback import print_exc


# TODO: Remove error reaction on success.


class Reaction(Cog):
    """Events related to reacting to messages
"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.bot.process_commands(after)

    @commands.Cog.listener()
    async def on_message(self, m):
        isbot = m.author.id == self.bot.user.id
        if isbot:
            await m.add_reaction(emoji="♻")

    @commands.Cog.listener()
    async def on_command(self, c):
        # Add reaction commands to bot response.
        try:
            botpfx = self.bot.config["prefixes"]
            if any([c.message.content.startswith(f'{x}quit') for x in botpfx]):
                return

            await c.message.add_reaction(emoji="🗜")
            await c.message.add_reaction(emoji="♻")
        except NotFound as e:
            print_exc(e)

    @commands.Cog.listener()
    async def on_command_error(self, command, error):
        # Delete invalid bot command
        cmdnotfound = type(error) == commands.CommandNotFound
        isDM = isinstance(command.channel, DMChannel)
        if cmdnotfound and not isDM:
            await command.message.delete()

    @commands.Cog.listener()
    async def on_reaction_add(self, r, user):
        try:
            if user.id != self.bot.user.id:
                # Erase message
                if r.emoji == "♻":
                    try:
                        if isinstance(r.message.channel, DMChannel):
                            return

                        rperc = r.count > len(r.message.channel.members) / 3
                        if rperc or user.id == self.bot.owner_id:
                            await r.message.delete()
                    except AttributeError:
                        await r.message.delete()

                # Rerun command
                elif r.emoji == "🗜" and user.id == r.message.author.id:
                    try:
                        for r in r.message.reactions:
                            await r.message.clear_reaction(r)
                    finally:
                        await self.bot.process_commands(r.message)
        except Forbidden as e:
            print(e)
            # cannot remove DM user reacts maybe remove instead of clear?

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        # Re-run a command when reaction is re-clicked. Check for cmds
        if user.id != self.bot.user.id:  # and reaction.emoji == "🗜":
            await self.on_reaction_add(reaction, user)

    @commands.command()
    @commands.is_owner()
    async def react(self, ctx, em: str):
        try:
            await ctx.message.mentions[0].send(em)
        finally:
            await ctx.message.add_reaction(emoji=em)


def setup(bot):
    bot.add_cog(Reaction(bot))
