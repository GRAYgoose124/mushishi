import json
from os import path
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Cog


class RoleRPG(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.rpg_file = path.join('plugins', 'resources', 'data', 'rpg.json')
        self.rpg_data = {}  # players, locations, items, spells
        self.rpg_channel = ''
        self.rpg_messages = {}

        self.object_thumbs = {}

        # List of messasges with pointers, etc
        self.rpg_events = {}

        self.locations = ['town', 'dungeon']
        self.events = ['battle', 'move']
        self.event_modifiers = ['ambush', ]

        try:
            with open(self.rpg_file, 'r') as f:
                self.rpg_data = json.load(f)
        except IOError:
            pass

    def __unload(self):
        with open(self.rpg_file, 'w') as f:
            json.dump(self.rpg_data, f)

    async def rpg_send(self, ctx, title, description,
                       content, tags: list, image='', thumb=''):
        em = Embed(title=title, description=description, colour=0xbada55)
        em.set_image(url=image)
        em.set_thumbnail(url=thumb)

        message = await ctx.send(content=content, embed=em)
        self.rpg_messages[message.id] = tags

        if 'battle' in self.rpg_messages[message.id]:
            await message.add_reaction(emoji='⚔')
            await message.add_reaction(emoji='🛡')
            await message.add_reaction(emoji='🌟')
            await message.add_reaction(emoji='❤')
            await message.add_reaction(emoji='🔥')
        if 'town' in self.rpg_messages[message.id]:
            await message.add_reaction(emoji='🏛')

    async def update_rpg(self, ctx, message):
        pass

    @commands.command()
    async def test_rpg(self, ctx):
        await self.rpg_send(ctx, 'Raider Attack', "It\'s an ambush!",
                                 "Get ready to fight!", ['battle'])
        await self.rpg_send(ctx, 'Dobrachev', "Town",
                                 "Relax man, it's civil here.", ['town'])

    async def on_reaction_add(self, reaction, user):
        reacteduser = reaction.message.author.id == user.id
        if reaction.message.id in self.rpg_messages and reacteduser:
            if 'battle' in self.rpg_messages[reaction.message.id]:
                if reaction.emoji == '⚔':
                    pass
                    # attack
                elif reaction.emoji == '🛡':
                    pass
                    # block
                elif reaction.emoji == '🌟':
                    pass
                    # special
                elif reaction.emoji == '❤':
                    pass
                    # heal
                elif reaction.emoji == '🔥':
                    pass
                    # cast
            if 'town' in self.rpg_messages[reaction.message.id]:
                if reaction.emoji == '🏛':
                    pass
                    # guild home
                else:
                    pass


def setup(bot):
    bot.add_cog(RoleRPG(bot))
