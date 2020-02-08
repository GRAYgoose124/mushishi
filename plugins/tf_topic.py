class TfTopic:
    def __init__(self, bot):
        self.bot = bot
        self.chat_history = []


def setup(bot):
    bot.add_cog(TfTopic(bot))
