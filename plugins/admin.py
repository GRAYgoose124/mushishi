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
from discord.ext.commands import (Cog,
                                  ExtensionAlreadyLoaded,
                                  ExtensionError,
                                  ExtensionNotFound,
                                  ExtensionFailed)
import traceback
import os

class Admin(Cog):
    """Commands related to plugin administration functionality.
    Many require owner/admin permissions.
    """
    def __init__(self, bot):
        self.bot = bot
        self.interactive = False

        self._get_all_plugins()

    async def on_command(self, command):
        real_prefix = command.message.content[:2]
        anyprfx = any([real_prefix == x for x in self.bot.config['prefixes']])
        if self.interactive and anyprfx:
            if hasattr(command, 'message'):
                await command.message.delete()

    @commands.group(pass_context=True)
    async def p(self, ctx):
        """<ld|rm|ls> [plugin_name]"""
        pass

    @p.command()
    @commands.is_owner()
    async def ld(self, ctx, plugin: str):
        """ <name> - load a pod """
        try:
            if plugin in self.bot.config['all_plugins']:
                raise ValueError

            await self.rm(ctx, plugin)
            self.bot.load_extension(f'plugins{plugin}')
            print(f"{plugin} loaded.")
            
            if '🔴' in ctx.message.reactions:
                await ctx.message.remove_reaction(emoji='🔴')
            await ctx.message.add_reaction(emoji='✅')
        except Exception as e:
            if isinstance(e, ExtensionError):
                traceback.print_tb(e.__traceback__)
            if isinstance(e, ExtensionFailed):
                print(e.args)
            if isinstance(e, ExtensionAlreadyLoaded):
                print("Pod reload failed. (Not unloaded)")
            if isinstance(e, ExtensionNotFound) or isinstance(e, ValueError):
                await ctx.send("No such pod exists.")

            if '✅' in ctx.message.reactions:
                await ctx.message.remove_reaction(emoji='✅')
            await ctx.message.add_reaction(emoji='🔴')

    @p.command()
    @commands.is_owner()
    async def rm(self, ctx, plugin: str):
        """ <name> - unload a pod """
        if plugin == "admin":
            await ctx.message.add_reaction(emoji='🚫')
        elif plugin in [x.lower() for x in self.bot.cogs.keys()]:
            self.bot.unload_extension(f'plugins.{plugin}')
            # delete pycache?
            print(f'{plugin} unloaded.')

    @p.command()
    async def ls(self, ctx):
        """ - list all available pods."""
        self._get_all_plugins()
       
        ps = ""
        for plugin in self.bot.config['all_plugins']:
            plugin = plugin.strip("*")
            if plugin in [x.lower() for x in self.bot.cogs.keys()]:
                ps += f'(✓) {plugin}\n'
            else:
                ps += f'( ) {plugin}\n'

        cogs = list(self.bot.cogs.keys())
        await ctx.send(f'My plugins are:\n{ps}\ncogs: {cogs}')

    @commands.command()
    @commands.is_owner()
    async def quit(self, ctx):
        """ shutdown mushishi """
        await ctx.bot.logout()

    @commands.Cog.listener()
    async def on_ready(self):
        print('---Loading plugins---')

        for plugin in self.bot.config['default_plugins']:
            try:
                self.bot.load_extension(f'plugins.{plugin}')
                print(f'Loaded {plugin}...')
            except Exception as e:
                print(e)

        print('Done loading plugins.')
        print('---Finished Starting---')

    def _get_all_plugins(self):
        self.bot.config['all_plugins'] = filter(lambda x: False if x is None else True, 
                                                [name[:-3] if '.py' in name else None 
                                                    for name in os.listdir(f"{os.getcwd()}/plugins") ])


def setup(bot):
    bot.add_cog(Admin(bot))


def teardown(bot):
    print("---Shutting down plugins---")
    for plugin in bot.loaded_plugins:
        print(f'Unloading {plugin}...')
        try:
            bot.unload_extension(plugin)
        except AttributeError as e:
            traceback.print_tb(e.__traceback__)
