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
from discord.ext.commands import Cog, ExtensionAlreadyLoaded, ExtensionError, ExtensionNotFound, ExtensionFailed
import traceback


class Admin(Cog):
    """Commands related to administration functionality.
    Many require owner/admin permissions.
    """
    def __init__(self, bot):
        self.bot = bot
        self.loaded_plugins = []
        self.interactive = False

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
            await self.rm(ctx, plugin)
            self.bot.load_extension(f'plugins.{plugin}')
            self.loaded_plugins.append(plugin)
            print(f'{plugin} loaded.')
            await ctx.message.add_reaction(emoji='✅')
        except ExtensionError as e:
            traceback.print_tb(e.__traceback__)
        except ExtensionFailed as e:
            print(e)
            traceback.print_tb(e.__traceback__)
        except ExtensionAlreadyLoaded:
            print("Pod reload failed. (Not unloaded)")
        except ExtensionNotFound:
            await ctx.send("No such pod exists.")
        except Exception as e:
            if '✅' in ctx.message.reactions:
                await ctx.message.remove_reaction(emoji='✅')
            await ctx.message.add_reaction(emoji='🔴')
            traceback.print_tb(e.__traceback__)

    @p.command()
    @commands.is_owner()
    async def rm(self, ctx, plugin: str):
        """ <name> - unload a pod """
        if plugin == "admin":
            await ctx.message.add_reaction(emoji='🚫')
        elif plugin in self.loaded_plugins:
            self.bot.unload_extension(f'plugins.{plugin}')
            print(f'{plugin} unloaded.')

            i = self.loaded_plugins.index(plugin)
            del(self.loaded_plugins[i])

            await ctx.message.add_reaction(emoji='✅')

    @p.command()
    async def ls(self, ctx):
        """ - list all available pods. *=active"""
        ps = ""
        for plugin in self.bot.config['plugins']:
            plugin = plugin.strip("*")
            if plugin in self.loaded_plugins:
                ps += f'(✓) {plugin}\n'
            else:
                ps += f'( ) {plugin}\n'

        await ctx.send(f'My plugins are:\n`{ps}`')

    @commands.command()
    @commands.is_owner()
    async def quit(self, ctx):
        """ shutdown mushishi """
        await ctx.bot.logout()

    @commands.Cog.listener()
    async def on_ready(self):
        print('---Loading plugins---')
        self.loaded_plugins = []
        for plugin in self.bot.config['plugins']:
            autoload = plugin[0] == '*'
            if autoload:
                plugin = plugin[1:]
                try:
                    self.bot.load_extension(f'plugins.{plugin}')
                    self.loaded_plugins.append(plugin)
                    print(f'Loaded {plugin}...')
                except Exception as e:
                    print(e)
        print('Done loading plugins.')
        print('---Finished Starting---')


def setup(bot):
    bot.add_cog(Admin(bot))


def teardown(bot):
    print("---Shutting down---")
    for plugin in self.loaded_plugins:
        print(f'Unloading {plugin}...')
        try:
            bot.unload_extension(plugin)
        except AttributeError as e:
            print_exc(e)