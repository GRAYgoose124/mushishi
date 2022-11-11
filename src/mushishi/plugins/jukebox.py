import asyncio
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
        self.queue = []

        music_dir = os.path.join(self.bot.resource_path, 'music')
        if not os.path.isdir(music_dir):
            os.mkdir(music_dir)
        if not os.path.isfile(self.bot.ch_path):
            with open(self.ch_path, mode='w+'):
                pass
    
    @commands.group(pass_context=True)
    async def yt(self, ctx):
        """ Youtube jukebox commands """
        pass
    
    @yt.command()
    async def playing(self, ctx):
        """ Get the currently playing song. """
        if ctx.voice_client.is_playing():
            await ctx.send(f"Now playing: {self.currently_playing}")
        else:
            await ctx.send("Nothing is playing.")

    @yt.command()
    async def queue(self, ctx):
        """ List the current queue. """
        pretty_queue = '\n'.join([f"{i+1}. {title}" for i, (title, _) in enumerate(self.queue)])
        await ctx.send(f"Current queue: {pretty_queue}")

    def play_next(self, ctx):
        if len(self.queue) > 0:
            now_playing = self.queue.pop(0)
            self.currently_playing = now_playing[0]

            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(now_playing[1]))
            ctx.voice_client.play(source, after=lambda _: self.play_next(ctx))

    async def play_result(self, ctx, result):
        author = ctx.message.author
        voice_channel = author.voice.channel

        title = result['entries'][0]['title']

        fn = result['entries'][0]['id'] + '.' + result['entries'][0]['ext']
        fp = os.path.join(self.bot.resource_path, 'music', fn)
        self.queue.append((title, fp)) 

        if self.vc is None or self.vc.channel.id != voice_channel.id:
            self.vc = await voice_channel.connect()

        if ctx.voice_client.is_playing():
            await ctx.send(f"Queued for play (#{len(self.queue)}): {title}")
        else:
            await ctx.send(f"Now playing: {title}")
            self.play_next(ctx)

    @yt.command(pass_context=True)
    async def play(self, ctx, *search):
        """ Plays the first result from a youtube search, or adds it to the queue. """
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

        # result = None
        # with YoutubeDL(ydl_opts) as ydl:
        #     result = ydl.extract_info(search)

        # await self.play_result(ctx, result)

        future = self.bot.loop.run_in_executor(None, YoutubeDL(ydl_opts).extract_info, search)
        future.add_done_callback(lambda f: asyncio.ensure_future(self.play_result(ctx, f.result())))


async def setup(bot):
    await bot.add_cog(Jukebox(bot))


async def teardown(bot):
    await bot.vc.disconnect()
    bot.vc = None