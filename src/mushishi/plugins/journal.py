# import json
# from os import path
# from discord.ext import commands
from discord.ext.commands import Cog


class DiaryBot(Cog):
    def __init__(self, bot):
        self.bot = bot

    def det_mood(self, user):
        pass

    def context(self, message):
        pass


async def setup(bot):
    await bot.add_cog(DiaryBot(bot))
