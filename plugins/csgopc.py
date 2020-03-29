from bs4 import BeautifulSoup as bs
import requests
import urllib3

from discord.ext import commands
from discord.ext.commands import Cog


class CSGOPC(Cog):
    csdeals_ss_url = r'https://cs.deals/screenshot'
    req_url = r'https://cs.deals/ajax/makeScreenshotRequest'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
        }


    def __init__(self, bot):
        self.bot = bot
        self.session = requests.Session()'ve e b'
    @commands.command()
    async def pricecheck(self, ctx, *url):
        if isinstance(url, list):
            url = ''.join(url)

        # Input Item
        item_url = ctx.message.content
        self.session.post(self.req_url, data={'link': item_url})

        # wait for last item to be processed
        #
        ss_page = self.session.get(self.csdeals_ss_url)
        my_shots = bs.find_all('div', {'class': 'button green copylink'})
        # get last screenshot created
        last_shot_url = None

        await ctx.send(last_shot_url)

def setup(bot):
    bot.add_cog(Rolemaster(bot))
