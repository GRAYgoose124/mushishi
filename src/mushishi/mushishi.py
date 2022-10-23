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
import discord
from discord.ext import commands
from pathlib import Path
from io import UnsupportedOperation


try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


class Mushishi(commands.Bot):
    def __init__(self, config_path):
        self.config = {}
        self.chat_history = None
        self.__config_setup(config_path)

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.plugins_path = os.path.join(self.dir_path, 'plugins')
        self.resource_path = os.path.join(self.dir_path, 'plugins',
                                          'resources')
        self.data_path = os.path.join(self.resource_path, 'data')
        self.ch_path = os.path.join(self.data_path, 'chat_history.json')

        if not os.path.isfile(self.ch_path):
            # TODO: Update all to use Paths.
            Path(self.ch_path).touch()

        # Load chat history
        # use append mode so that if the file doesn't exist, we create it.
        with open(self.ch_path, mode='a') as f:
            try:
                self.chat_history = json.load(f)
            # TODO: Don't use exceptions for this task.
            except (json.JSONDecodeError, UnsupportedOperation) :
                self.chat_history = {}

        # Intents Patch TODO: review
        intents = discord.Intents.all()

        super().__init__(self.config['prefixes'], intents=intents)

    def __config_setup(self, config_path):
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            src_url = 'https://github.com/GRAYgoose124/mushishi'
            self.config = {"token": "<TOKEN>",
                           'default_plugins': ["utils", "reaction"],
                           'prefixes': ["m.", "mu ", "\N{BUG} "],
                           'source_url': src_url,
                           'resource_host': ""
                           }

            with open(config_path, 'w') as f:
                json.dump(self.config, f)

            raise FileNotFoundError("Please edit the generated config file.")

    async def on_message(self, m):
        bpfx = any([m.content.startswith(x) for x in self.config['prefixes']])
        me = m.author.id == self.user.id
        if not bpfx and not me and m.content != '':
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

    async def on_ready(self):
        print('Logged in as {0} ({0.id})'.format(self.user))

    def save_chat(self):
        print("Core: Saving messages...")
        with open(self.ch_path, mode='w+') as f:
            json.dump(self.chat_history, f, sort_keys=True)
        print("Core: Done saving.")

    def run(self):
        self.load_extension('plugins.admin')

        super().run(self.config['token'])
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.start(self.config['token'], bot=True))

        self.save_chat()
