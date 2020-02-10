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
import random
from time import time
import numpy as np
from matplotlib import pyplot as plt
# import scipy
# import scipy.integrate as integrate
from discord import Embed
from discord.ext import commands
from os import path
from discord.ext.commands import Cog


class EquationGraph:
    def __init__(self):
        pass

    def parse(self, equation):
        pass


class Calc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def calc(self, ctx):
        """ [solve|rpn] - Calculators and Solvers.
        """

    @calc.command()
    async def solve(self, ctx, equation: str):
        print(equation)
        ctx.send(f'```{equation}```')

    @commands.command()
    async def randn(self, ctx, dice_size: int):
        random.seed(time.time())
        result = int(random.random() * dice_size) + 1
        await ctx.send(f'Rolled {result}')

    @calc.command()
    async def rpn(self, ctx, *equation: str):
        """<equation> : RPN calculator"""
        response = None

        stack = []
        for op in equation:
            try:
                v = float(op)
                stack.append(v)
            except ValueError:
                try:
                    if op == 'pi':
                        stack.append(np.pi)
                    elif op == 'e':
                        stack.append(np.e)
                    else:
                        a = stack.pop()
                        if op == '+':
                            b = stack.pop()
                            stack.append(a + b)
                        elif op == '-':
                            b = stack.pop()
                            stack.append(b - a)
                        elif op == '*':
                            b = stack.pop()
                            stack.append(a * b)
                        elif op == '^':
                            b = stack.pop()
                            if b < 10 ** 10:
                                stack.append(a ** b)
                        elif op == '|':
                            b = stack.pop()
                            t = a ** b
                            stack.append(a ** t)
                        elif op == '/':
                            b = stack.pop()
                            stack.append(b / a)
                        elif op == 'sin':
                            stack.append(np.sin(a))
                        elif op == 'cos':
                            stack.append(np.cos(a))
                except IndexError:
                    response = "Invalid RPN \"{}\", {}".format(equation, stack)

        response = stack

        await ctx.send(response)


class Plot(Cog):
    def __init__(self, bot):
        self.bot = bot

    def _plot_equation(self, equation, x_view=10, x_res=0.01, image=False):
        """"""
        x = np.arange(-x_view, x_view, x_res)
        plt.clf()

        try:
            plot = plt.plot(x, equation(x))
        except Exception:
            return

        try:
            if not image:
                fig = plt.show(plot)
                return fig
            else:
                dir_path = path.dirname(path.realpath(__file__))
                p = path.join(f'images/tmp_plots/plot{time()}.png')
                image = path.join(dir_path, 'resources', p)
                with open(image, 'wb+') as f:
                    plt.savefig(f,
                                facecolor=(0, 0, 0, .30),
                                transparent=True,
                                format='png',
                                bbox_inches='tight',
                                pad_inches=0.0)
                return p
        except IOError as e:
            print(e)

    # Todo: Cache images
    @commands.command()
    @commands.is_owner()
    async def plot(self, ctx, *python_in: str):
        """[equation] - plots an equation if valid."""
        python_in = ' '.join(python_in)

        valid_eq = None
        p = self._plot_equation(valid_eq, image=True)

        rh = self.bot.config['resource_host']
        url = f'http://{rh}/{p}'

        await ctx.send(embed=Embed(colour=0xBADA55,
                                   description=valid_eq).set_image(url=url))


def setup(bot):
    bot.add_cog(Calc(bot))
    bot.add_cog(Plot(bot))
