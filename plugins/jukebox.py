from discord.ext.commands import Cog
from discord.ext import commands
from discord.player import FFmpegOpusAudio
from youtube_dl import YoutubeDL
import os


class Jukebox(Cog):
    def __init__(self, bot):
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

        try:
            self.vc = await voice_channel.connect()
        except Exception as e:
            print(e)

        if self.vc is not None:
            fp = os.path.join(self.bot.resource_path,
                              'videos', '%(title)s.%(ext)s')

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': fp,
                'noplaylist': True,
                'progress_hooks': [self.get_fn],
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

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([search])

            try:
                aus = FFmpegOpusAudio(self.currently_playing)
                player = self.vc
                player.play(aus)
            except Exception as e:
                print(e)




def setup(bot):
    bot.add_cog(Jukebox(bot))

def teardown(bot):
    bot.vc.disconnect()
    bot.vc = None