import json
from os import path
from discord.ext.commands import Cog


class Rolemaster(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.role_file = path.join('plugins', 'resources', 'role_stats.json')
        self.role_data = {}
        try:
            with open(self.role_file, 'r') as f:
                self.role_data = json.load(f)
        except IOError:
            pass

    def __unload(self):
        with open(self.role_file, 'w') as f:
            json.dump(self.role_data, f)


def setup(bot):
    bot.add_cog(Rolemaster(bot))
