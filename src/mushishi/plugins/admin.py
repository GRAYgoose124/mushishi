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
import logging




class Admin(Cog):
    """Commands related to plugin administration functionality.
    Many require owner/admin permissions.
    """
    def __init__(self, bot):
        self.logger = bot.logger.getChild("plugin/admin")
        self.logger.debug('Initializing Admin cog.')
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
            if plugin not in self.bot.config['all_plugins']:
                print(plugin, 'not in', self.bot.config['all_plugins'])
                raise ValueError
            
            await self.rm(ctx, plugin)
            # Change this to locate foreign plugins
            await self.bot.load_extension(f'mushishi.plugins.{plugin}')
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
                self.logger.warning(f"Plugin {plugin} not found.", exc_info=e)
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
            # TODO: change with L121 and 135
            await self.bot.unload_extension(f'mushishi.plugins.{plugin}')
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

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        """ shutdown mushishi """
        self.bot._restart = True
        raise KeyboardInterrupt

    @commands.Cog.listener()
    async def on_ready(self):
        print('---Loading plugins---')

        for plugin in self.bot.config['default_plugins']:
            try:
                # Can probably hack this to import foreign plugins
                await self.bot.load_extension(f'mushishi.plugins.{plugin}')
                print(f'Loaded {plugin}...')
            except Exception as e:
                print(e)

        print('Done loading plugins.')
        print('---Finished Starting---')

    def _get_all_plugins(self):
        cwd = os.path.join(os.path.dirname(__file__))
        all_dirs = os.listdir(f"{cwd}")
        site_plugin_dir = os.listdir(self.bot.plugins_path)
        all_dirs.extend(site_plugin_dir)

        print(all_dirs)
        self.bot.config['all_plugins'] = list(filter(lambda x: False if x is None else True, 
                                                [name[:-3] if '.py' in name else None 
                                                    # TODO modify this along with L:121 and the similar line in start.py
                                                    # ROOT issue.
                                                    for name in all_dirs]))


async def setup(bot):
    await bot.add_cog(Admin(bot))


async def teardown(bot):
    print("---Shutting down plugins---")
    for plugin in bot.loaded_plugins:
        print(f'Unloading {plugin}...')
        try:
           await bot.unload_extension(plugin)
        except AttributeError as e:
            traceback.print_tb(e.__traceback__)
