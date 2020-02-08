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
import json
import asyncio
import os
import re
from discord.ext import commands
from traceback import print_exc

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


class Mushishi(commands.Bot):
    def __init__(self, config_path):
        self.done = True
        self.chat_history = None
        self.config = {}
        self.loaded_plugins = []
        self.__config_setup(config_path)

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.plugins_path = os.path.join(self.dir_path, 'plugins')
        self.resource_path = os.path.join(self.dir_path, 'plugins',
                                          'resources')
        self.data_path = os.path.join(self.resource_path, 'data')
        self.ch_path = os.path.join(self.data_path, 'chat_history.json')

        if not os.path.isfile(self.ch_path):
            with open(self.ch_path, mode='w+'):
                pass

        with open(self.ch_path, mode='r') as f:
            try:
                self.chat_history = json.load(f)
            except json.JSONDecodeError:
                self.chat_history = {}

        super().__init__(command_prefix=self.config['prefixes'])

    def __config_setup(self, config_path):
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            src_url = 'https://github.com/GRAYgoose124/mushishi'
            self.config = {"token": "<TOKEN>",
                           'plugins': ["*admin", "*utils", "*reaction"],
                           'prefixes': ["m.", "mu ", "\N{BUG} "],
                           'source_url': src_url,
                           'resource_host': ""}

            with open(config_path, 'w') as f:
                json.dump(self.config, f)

            raise FileNotFoundError("Please edit the generated config file.")

        def __root_setup(self): pass

    def run(self):
        self.done = False
        super().run(self.config['token'])

    async def on_ready(self):
        print('---Starting---')
        self.loaded_plugins = []
        for plugin in self.config['plugins']:
            autoload = plugin[0] == '*'
            if autoload:
                plugin = plugin[1:]
                try:
                    self.load_extension(f'plugins.{plugin}')
                    self.loaded_plugins.append(f'plugins.{plugin}')
                    print(f'Loaded {plugin}...')
                except Exception as e:
                    print(e)
        print('Done loading plugins.')
        print('---Finished Starting---')

    async def on_message(self, m):
        tstcmd = [m.content.startswith(x) for x in self.config['prefixes']]
        notbot = m.author.id != self.user.id
        if not any(tstcmd) and notbot:
            chan_name = None
            smc = re.sub('[-:. ]', '', str(m.created_at))
            if not hasattr(m.channel, 'name'):
                chan_name = 'DM'
            else:
                chan_name = m.channel.name

            if chan_name not in self.chat_history:
                self.chat_history[chan_name] = {}
            self.chat_history[chan_name][smc] = (m.author.name, m.content)
            print(chan_name, smc, ':', self.chat_history[chan_name][smc])

        await self.process_commands(m)

    async def close(self):
        if self.done:  # hack because it's double closing :/
            return

        print("---Shutting down---")
        for plugin in self.loaded_plugins:
            print(f'Unloading {plugin}...')
            try:
                self.unload_extension(plugin)
            except AttributeError as e:
                print_exc(e)

        print("Core: Saving messages...")
        with open(self.ch_path, mode='w+') as f:
            json.dump(self.chat_history, f, sort_keys=True)
        print("Core: Done saving.")
        self.done = True

        await super().close()


if __name__ == '__main__':
    config_path = 'config.json'
    bot = Mushishi(config_path)
    bot.run()
