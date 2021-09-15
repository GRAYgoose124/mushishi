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
from time import time
import re
from discord.ext import commands
from discord import Embed
import sqlalchemy as sa
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Text
from sqlalchemy.sql.expression import func
# import nltk
from discord.ext.commands import Cog


# TODO: chain triggers, event triggers,
# TODO: periodic/randomized triggers, limited self-trigger
# TODO: morphological/lexical transformations, markov permutations
# TODO: conv->factoid gen


dir_path = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(dir_path, 'resources', 'data', 'facts.db')
if os.name == 'nt':
    db_path = f'sqlite:///{db_path}'
else:
    db_path = f'sqlite:////{db_path}'


# create a regex function for sqlite and import it
@sa.event.listens_for(sa.engine.Engine, 'connect')
def sqlite_engine_connect(dbapi_conn, connection_record):
    dbapi_conn.create_function('regexp', 2, _regexp)


def _regexp(expr, item):
    if item is None:
        return
    try:
        reg = re.compile(expr, re.I)
        return reg.search(item) is not None
    except re.error:
        pass


# init db
Base = declarative_base()


class Fact(Base):
    __tablename__ = 'facts'
    id = Column(Integer, primary_key=True)
    fact = Column(Text, nullable=False)
    response = Column(Text, nullable=False)


engine = create_engine(db_path)
Fact.metadata.create_all(engine)
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()  #


class FactoidGen:
    def __init__(self):
        pass

    def find_recurrences(self):
        pass


class Factoid(Cog):
    """Factoids are short definitions for actions that a bot can
        trigger. Usually text responses.
    """
    def __init__(self, bot):
        self.bot = bot
        self.last_triggered = {}

    @commands.group(pass_context=True)
    async def fact(self, ctx):
        """ [add|remove|find] - Simple pattern-based replies.
        """
        pass

    @fact.command()
    async def add(self, ctx, *fact: str):
        """ <fact> <action> <response> - Create a new factoid."""
        fact = ' '.join(fact).split(' >> ')
        if len(fact) == 2:
            session.add(Fact(fact=fact[0], response=fact[1]))
            session.commit()
            await ctx.send(f'Factoid: ``{fact}`` saved.')
        else:
            await ctx.send(f'`{fact}` was malformed. RTFM.')

    @fact.command()
    @commands.is_owner()
    async def rm(self, ctx, fact_id: int):
        """ <id> - Removes a factoid by id."""
        factoid = session.query(Fact).get(fact_id)
        factoid_str = f'{factoid.id}: {factoid.fact} -> {factoid.response}\n'
        factoid.delete()
        session.commit()
        await ctx.send(f'Factoid: `{factoid_str}` deleted.')

    @fact.command()
    async def find(self, ctx, q: str):
        """ <query> - Find a factoid by a substring."""
        results = ''

        if q is None:
            pass
        else:
            f = Fact.fact.like(f'%{q}%') | Fact.response.like(f'%{q}%')
            for result in session.query(Fact).filter(f):
                results += f'{result.id}: {result.fact} -> {result.response}\n'

        await ctx.send(embed=Embed(
            description=f'Here is what I found:\n```{results}```\n\n'))

    @fact.command()
    async def get(self, ctx, index: int):
        for result in session.query(Fact).filter(Fact.id):
            d = f'```{result.fact} -> {result.response}```\n'
            await ctx.send(embed=Embed(title=f'Fact {index}', description=d))

    @commands.Cog.listener()
    async def on_message(self, m):
        if m.author.bot:
            return

        factoid = session.query(Fact)\
            .filter(Fact.fact.op('REGEXP')(f'{m.content}'))\
            .order_by(func.random())\
            .first()

        if factoid is not None and factoid.response != '<NONE>':
            if factoid.id not in self.last_triggered:
                self.last_triggered[factoid.id] = time() - 450
            if time() - self.last_triggered[factoid.id] < 450:
                return
            else:
                await m.channel.send(factoid.response)
                self.last_triggered[factoid.id] = time()


def setup(bot):
    bot.add_cog(Factoid(bot))


def teardown(bot):
    print('Factoid: Committing db.')
    session.commit()
    print('Factoid: Closing db.')
    session.close()
    print('Factoid: Done.')
