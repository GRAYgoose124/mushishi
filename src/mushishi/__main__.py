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
import argparse
from .mushishi import Mushishi, BotRestart


LOG_LEVELS = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR, 'CRITICAL': logging.CRITICAL}


def argparser():
    parser = argparse.ArgumentParser(description="Mushishi: A smart discord bot using the discord.py[rewrite] API.")
    parser.add_argument('-L', '--log-level', dest='log_level', default='INFO', help='Set the log level.')
    parser.add_argument('-q', '--quiet', dest='quiet', default=False, action='store_true', help='Silence STDOUT logging.')
    parser.add_argument('--passthrough-logging', dest='passthrough_logging', default=False, action='store_true', help='Disable passthrough logging to STDOUT.')
    
    return parser.parse_args()


def get_config_path(custom_dir=None):
    """Get the path to the config file."""

    # get user home directory from $XDG_CONFIG_HOME or $HOME
    if os.getenv('XDG_CONFIG_HOME'):
        config_dir = os.path.join(os.getenv('XDG_CONFIG_HOME'), custom_dir or 'mushishi')
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
    else:
        config_dir = custom_dir or os.path.join(os.getenv('HOME'), '.mushishi')
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
    args = argparser()
    config_dir = get_config_path()

    # set up logging
    log_file = os.path.join(config_dir, 'mushishi.log')
    log_level = LOG_LEVELS.get(args.log_level.upper(), logging.INFO) or logging.INFO

    logger = logging.getLogger('mushishi')
    logger.setLevel(log_level)

    logging.basicConfig(level=log_level, format='%(name)s\t%(message)s')
        
    file_handler = logging.FileHandler(log_file)
    file_handler.addFilter(logging.Filter('mushishi'))
    logger.addHandler(file_handler)

    if not args.quiet:
        stream_handler = logging.StreamHandler(sys.stdout)
        if not args.passthrough_logging:
            stream_handler.addFilter(logging.Filter('mushishi'))

        logger.addHandler(stream_handler)

    # Grab our event loop and initalize the bot.
    loop = asyncio.get_event_loop()
    bot = Mushishi(config_dir, parent_logger=logger, loop=loop)

    # Lets create a task handle to run the bot so we can easily restart it.
    bot_task = loop.create_task(bot.start())
    try:
        print("\t--\tWelcome to Mushishi!\tEnjoy your bug-catching experience!\t--")

        loop.run_until_complete(bot_task)
    except KeyboardInterrupt as _e:
        loop.run_until_complete(bot.logout())
        bot_task.cancel()

        if hasattr(bot, '_restart'):
            if bot._restart:
                question = 'y'
            else: 
                question = 'N'
        else:
            question = input("Restart? [y/N] ")

        if question.lower() == 'y':
            # _restart is used by plugins.admin.restart to skip question
            bot._restart = False
            print("Restarting...")
            main()
        else:
            # Just exit properly if they don't want to restart.
            loop.close()
            sys.exit(0)    
    finally:
        print("\t--\tShutdown complete\t--\n{}Goodbye... \U0001F41B".format("\t"*15))

 


if __name__ == '__main__':
    main()

