from discord.ext.commands import Cog
from discord.ext import commands
import discord
from youtube_dl import YoutubeDL
import os


class Jukebox(Cog):
    def __init__(self, bot):
        self.logger = bot.logger.getChild("plugin/jukebox")
        self.logger.debug('Initializing Admin cog.')

        self.bot = bot
        self.vc = None
        self.currently_playing = None

        vd = os.path.join(self.bot.resource_path, 'videos')
        if not os.path.isdir(vd):
            os.mkdir(vd)
        if not os.path.isfile(self.bot.ch_path):
            with open(self.ch_path, mode='w+'):
                pass

    @commands.command(pass_context=True)
    async def yt(self, ctx, *search):
        author = ctx.message.author
        voice_channel = author.voice.channel
        search = (' ').join(search)


        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.bot.resource_path,
                            'music', '%(id)s.%(ext)s'),
            'noplaylist': True,
            'progress_hooks': [],
            'default_search': "ytsearch",
            'max_downloads': 1,
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': True,
            'quiet': False,
            'no_warnings': True,
            'source_address': '0.0.0.0'
        }

        result = None
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(search)

        print(result['entries'][0])   
        fn = result['entries'][0]['id'] + '.' + result['entries'][0]['ext']
        fp = os.path.join(self.bot.resource_path, 'music', fn)
        
        try:
            self.vc = await voice_channel.connect()
        except Exception as e:
            print(e)

        try:
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(fp))
            ctx.voice_client.play(
                source, after=lambda e: print("Player error: %s" % e) if e else None
            )
        except Exception as e:
            print(e)

        await ctx.send(f"Now playing: {result['entries'][0]['title']}")


async def setup(bot):
    await bot.add_cog(Jukebox(bot))

async def teardown(bot):
    bot.vc.disconnect()
    bot.vc = None