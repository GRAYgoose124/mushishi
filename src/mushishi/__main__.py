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
from .mushishi import Mushishi


def get_config_path():
    if os.getenv('XDG_CONFIG_HOME'):
        config_dir = os.path.join(os.getenv('XDG_CONFIG_HOME'), 'mushishi')
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
    else:
        config_dir = os.path.join(os.getenv('HOME'), '.config', 'mushishi')
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)

    return os.path.join(config_dir, 'config.json')


# rerun = True
def main():
    # global rerun
    # while True:
    # get user home directory from $XDG_CONFIG_HOME or $HOME
    bot = Mushishi(get_config_path())
        # @commands.is_owner()
        # @bot.command(pass_context=True)
        # async def restart(ctx):
        #     global rerun
        #     await bot.logout()
        #     time.sleep(10)
        #     rerun = True
        #
        #
        # @commands.is_owner()
        # @bot.command(pass_context=True)
        # async def shutdown(ctx):
        #     await bot.logout()
        # if rerun:
    bot.run()
    #     rerun = False
    print("---Shutdown complete---\nGoodbye.")



if __name__ == '__main__':
    main()

