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
import time
import traceback
import ast
from os import path
import json
import re
from discord import Embed, Colour, NotFound
from discord.ext import commands
from discord.ext.commands import Cog


class Utils(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_absence = {'checked': 0, 'average': 0}
        self.last_command = None
        self.uptime = time.clock()
        self.status_timestamps = {}

        # Bot thumbnail
        rh = self.bot.config['resource_host']
        bt = path.join('images', 'thumbnails', 'bot_stats.png')
        self.__bot_thumb = f'http://{rh}/{bt}'

        st = path.join('images', 'thumbnails', 'source.png')
        self.__src_thumb = f'http://{rh}/{st}'

        pt = path.join('images', 'thumbnails', 'poll.png')
        self.__pol_thumb = f'http://{rh}/{pt}'

    @commands.command()
    async def stats(self, ctx):
        app_info = await self.bot.application_info()

        t = (time.clock() - self.uptime)
        m, s = divmod(t, 60)
        h, m = divmod(m, 60)
        d = h / 24

        desc = (f'Owner: {app_info.owner.name}\n',
                f'Uptime: {round(d)} days, {h} hours',
                f'{round(m)} minutes, {round(s)} seconds\n')
        em = Embed(title="Stats",
                   description=desc,
                   colour=Colour(0xBADA55)).set_thumbnail(url=self.__bot_thumb)

        await ctx.send(embed=em)

    @commands.command()
    async def source(self, ctx):
        em = Embed(title="Source code",
                   url=self.bot.config['source_url'],
                   colour=Colour(0xBADA55),
                   type='rich').set_thumbnail(url=self.__src_thumb)
        await ctx.send(embed=em)

    @commands.command()
    @commands.is_owner()
    async def vanish(self, ctx):
        """ - clears mushishi\'s recent history"""
        async for message in ctx.channel.history(limit=40):
            if message.author == self.bot.user:
                await message.delete()

    @commands.command()
    async def cleancmds(self, ctx):
        """Removes all commands user has typed."""
        async for message in ctx.channel.history(limit=20):
            if message.author.name == ctx.message.author.name and \
             any('🗜' == x.emoji or '♻' == x.emoji for x in message.reactions):
                try:
                    await message.delete()
                except NotFound:
                    pass

    @commands.is_owner()
    @commands.command()
    async def cleanall(self, ctx, name):
        """ <name> - clears recent messages from user"""
        async for message in ctx.channel.history(limit=100):
            if message.author.name == name:
                await message.delete()

    # @commands.command()
    # @commands.is_owner()
    # async def focus(self, ctx):
    #     """ - interactive mode"""
    #     if self.interactive:
    #         await self.clean(ctx, 3)
    #         if "mu focus" in ctx.message.content:
    #             self.interactive = False
    #     else:
    #         self.interactive = True

    @commands.command()
    @commands.is_owner()
    async def evil(self, ctx, *code: str):
        """ - eval python code"""
        try:
            code = ' '.join(code)

            for node in ast.walk(ast.parse(code)):
                isexpr = type(node) == ast.Expr
                iscall = type(node.value) == ast.Call
                iseval = node.value.func.id == 'eval'
                if type(node) == ast.Import:
                    await ctx.send(f'No importing! Only evil!')
                    return
                elif isexpr and iscall and iseval:
                    await ctx.send(f'No eval! Only evil!')
                    return

            results = eval(code)
            await ctx.send(f'{results}')
        except Exception as e:
            traceback.print_exc(e)
            await ctx.send(f'`{e.__class__.__name__}{e}\n'
                           f'{traceback.format_exc(e)}`')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        self.status_timestamps[after.id] = (time.clock(), after.status)



def setup(bot):
    bot.add_cog(Utils(bot))
