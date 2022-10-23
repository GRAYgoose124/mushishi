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
import os
import asyncio
import logging
import sys
from .mushishi import Mushishi, BotRestart


logger = logging.getLogger('main')


def get_config_path(custom_dir=None):
    """Get the path to the config file."""

    # get user home directory from $XDG_CONFIG_HOME or $HOME
    if os.getenv('XDG_CONFIG_HOME'):
        config_dir = os.path.join(os.getenv('XDG_CONFIG_HOME'), custom_dir or 'mushishi')
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
    else:
        config_dir = custom_dir or os.path.join(os.getenv('HOME'), '.config', 'mushishi')
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)

    return config_dir


# rerun = True
def main():
    """Main entry point for mushishi bot.

        This is what we target in pyproject.toml as our entry script.

        It runs the bot and handles any exceptions that may occur, providing
        a clean exit and easy restarting.

        It will not return in any case to a caller unless an exception occurs,
        in which case it will only reraise the exception, allowing the caller 
        to handle it. 

    """
    config_dir = get_config_path()

    logger.info("\t--\tWelcome to Mushishi!\tEnjoy your bug-catching experience!\t--")


    # Grab our event loop and initalize the bot.
    loop = asyncio.get_event_loop()
    bot = Mushishi(config_dir)

    # Lets create a task handle to run the bot so we can easily restart it.
    bot_task = loop.create_task(bot.start(bot.config['token']))
    try:
        loop.run_until_complete(bot_task)
    except Exception as any_exception:
        # For any exception, we want to full log out and cancel the task.
        bot_task.cancel()
        loop.run_until_complete(bot.logout())
        loop.run_until_complete(bot.close())

        # If the exception is a KeyboardInterrupt, we want to ask the user if
        # they want to restart the bot.
        if isinstance(any_exception, KeyboardInterrupt):
            question = input("Restart? [y/N] ")
            if question.lower() == 'y':
                logger.info("Restarting...")
                main()
            else:
                # Just exit properly if they don't want to restart.
                loop.close()
                sys.exit(0)    
        else:
            # If it's not a KeyboardInterrupt, we want to log the exception and
            # exit.
            logger.error(f"\t--\t Mushishi failed poorly\t-- {any_exception}")
            raise any_exception
    finally:
        logger.info("\t--\tShutdown complete\t--\n{}Goodbye... \U0001F41B".format("\t"*15))

 


if __name__ == '__main__':
    main()

