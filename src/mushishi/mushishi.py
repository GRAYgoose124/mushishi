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
import sys
import discord
from discord.ext import commands
import logging
from pathlib import Path
import io

try:
    if os.name == 'nt':
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass




SRC_URL = 'https://github.com/GRAYgoose124/mushishi'
DEFAULT_CONFIG = {"token": "<TOKEN>",
                    'default_plugins': ["utils", "reaction", "factoid"],
                    'prefixes': ["m.", "mu ", "\N{BUG} "],
                    'source_url': SRC_URL,
                    'resource_host': ""
                }


class BotRestart(Exception):
    pass


class Mushishi(commands.Bot):
    def __init__(self, config_path, loop=None, parent_logger=None):
        self.logger = parent_logger.getChild("bot") if parent_logger else None
        
        if self.logger is None:
            self.logger = logging.getLogger("mushishi")
            logging.basicConfig(level=logging.INFO)

        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        self.config = {}
        self.chat_history = None

        self.config_path = config_path
        self.plugins_path = os.path.join(self.config_path, 'plugins')
        self.resource_path = os.path.join(self.plugins_path, 'resources')
        self.data_path = os.path.join(self.resource_path, 'data')

        self.config_file = os.path.join(self.config_path, 'config.json')
        self.ch_path = os.path.join(self.data_path, 'chat_history.json')

        self.__config_setup()

        # Intents Patch TODO: review
        intents = discord.Intents.all()
        super().__init__(self.config['prefixes'], intents=intents)

    def __config_setup(self):
        """Setup the config file and directories."""
        # Create each directory if it doesn't exist.
        if not os.path.isdir(self.config_path):
            os.mkdir(self.config_path)
        if not os.path.isdir(self.plugins_path):
            os.mkdir(self.plugins_path)
        if not os.path.isdir(self.resource_path):
            os.mkdir(self.resource_path)
        if not os.path.isdir(self.data_path):
            os.mkdir(self.data_path)
            
        # Load the chat history.
        with open(self.ch_path, mode='r') as f:
            try:
                self.chat_history = json.load(f)
            # TODO: Don't use exceptions for this task.
            except (json.decoder.JSONDecodeError, io.UnsupportedOperation):
                print(self.logger)
                self.logger.info("Chat history file is empty.")
                self.chat_history = {}

        # Load config or generate a new one.
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = DEFAULT_CONFIG   

            # Dump default config to file.
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f)

            # Fail and tell the user to edit the config.
            raise FileNotFoundError("Please edit the generated config file to add your bot token.")

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
        with open(self.ch_path, mode='w') as f:
            json.dump(self.chat_history, f, sort_keys=True)
        print("Core: Done saving.")

    async def start(self):
        print("Core: Starting bot...")
        try:
            await self.load_extension('mushishi.plugins.admin')
        except Exception as e:
            self.logger.error('Failed to load admin plugin.', exc_info=e)

        try:
            await super().start(self.config['token'])
        except discord.LoginFailure:
            self.logger.error('Invalid token.')
        except BotRestart:
            raise BotRestart

    async def logout(self):
        self.save_chat()
        await super().close()