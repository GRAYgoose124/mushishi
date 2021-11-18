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
# import time
from mushishi import Mushishi
# from discord.ext import commands


# rerun = True


def main():
    # global rerun
    # while True:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(dir_path, 'config.json')
        bot = Mushishi(config_path)

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

