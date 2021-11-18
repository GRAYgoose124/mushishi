import json
from discord.ext import commands
from discord.ext.commands import Cog
import os
import time
import openai
import re
from os import path

# Todo: Posi-tagged history, only integrate history that has been flagged 
# Todo: generate prompts from filtered history, likely through lstm+cgans

openai.api_key = os.getenv("OPENAI_API_KEY")


stops = {'poems': ['---'], 'physics': ["Q:"]}


class GPT(Cog):
    def __init__(self, bot, history=False):
        self.bot = bot
        self.last_procced = time.time()

        self.prompts = json.load(open(path.join(self.bot.resource_path,
                                                "data/prompts.json"), 'r'))
        self.default_prompt = self.prompts['physics']
        self.stops = stops['physics']

        self.bhistory = history
        if self.bhistory:
            self.history = []
        else:
            self.history = None

        self.response_filter = re.compile('#.*#[0-9]+:(.*)')

    @commands.group(pass_context=True)
    async def pr(self, ctx):
        """prompts """
        pass

    @pr.command()
    async def new(self, ctx, prompt, *body):
        if prompt not in self.prompts and len(body) > 0:
            self.prompts[prompt] = body
            with open(path.join(self.bot.resource_path, "data/prompts.json"), "w+") as f:
                json.dump(self.prompts, f)

    @pr.command()
    async def set(self, ctx, prompt: str):
        self.default_prompt = self.prompts[prompt]
        self.stops = stops[prompt] if prompt in stops else []
        print(prompt, self.default_prompt)

    @commands.Cog.listener()
    async def on_message(self, m):
        if m.channel.name != 'bot-questions' or m.content[:2] == "m.":
            return

        if self.bhistory:
            self.history.append(m.content)
            if len(self.history) > 10:
                self.history.pop(0)

        if not m.author.bot and time.time() - self.last_procced > 3.0:
            s = f'{m.content}'  # todo generalize format/filter strings/re/etc

            if self.bhistory:
                s = "---".join(self.history)[:-1] + s

            prompt = self.default_prompt + s
            response = openai.Completion.create(
                engine="ada",
                prompt=prompt,
                temperature=0.7,
                max_tokens=120,
                top_p=1,
                frequency_penalty=0.3,
                presence_penalty=0.1,
                stop=self.stops
            )

            if response:
                await m.channel.send(response["choices"][0]["text"].strip())

            self.last_procced = time.time()


def setup(bot):
    bot.add_cog(GPT(bot))
