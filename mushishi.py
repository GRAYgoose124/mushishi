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
import time
from discord.ext import commands
from traceback import print_exc

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


class Mushishi(commands.Bot):
    def __init__(self, config_path):
        self.config = {}
        self.loaded_plugins = []
        self.__config_setup(config_path)

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.plugins_path = os.path.join(self.dir_path, 'plugins')
        self.resource_path = os.path.join(self.dir_path, 'plugins',
                                          'resources')
        self.data_path = os.path.join(self.resource_path, 'data')
        self.lm_path = os.path.join(self.data_path, 'last_messages.json')

        with open(self.lm_path, mode='w+') as f:
            try:
                self.last_messages = json.load(f)
            except json.JSONDecodeError:
                self.last_messages = {}

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
        super().run(self.config['token'])

    async def on_ready(self):
        self.loaded_plugins = []
        for plugin in self.config['plugins']:
            if plugin[0] == '*':
                plugin = plugin[1:]
                try:
                    self.load_extension(f'plugins.{plugin}')
                    self.loaded_plugins.append(f'plugins.{plugin}')
                    print(f'Loaded {plugin}...')
                except Exception as e:
                    print(e)
        print('Done loading plugins.')

    async def close(self):
        for plugin in self.loaded_plugins:
            print(f'Unloading {plugin}...')
            try:
                self.unload_extension(plugin)
            except AttributeError as e:
                print_exc(e)
        self.loaded_plugins = []

        self.clear()
        time.sleep(1)
        await super().close()
        print("Shutdown clean up complete.\nGoodbye.")


if __name__ == '__main__':
    config_path = 'config.json'
    bot = Mushishi(config_path)
    bot.run()
