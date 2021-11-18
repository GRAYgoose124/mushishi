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
import math
from discord.ext import commands
import numpy as np
# import sympy
# import plotly

# import plotly.graph_objects as go

from discord.ext.commands import Cog


class Network:
    def __init__(self, input_width, hidden_size, output_width):
        """Network(input_width, (n_hidden, hidden_width), output_width)"""
        self.hidden_size = hidden_size
        self.input_layer = np.zeros(input_width)
        self.hidden_layers = np.zeros((hidden_size[0], hidden_size[1]), float)
        self.output_layer = np.zeros(output_width)

        self.ih_weights = np.ones((hidden_size[0], input_width))
        self.hidden_weights = np.random.random_sample((hidden_size[0],
                                                       hidden_size[0],
                                                       hidden_size[1]))
        self.ho_weights = np.ones((output_width, hidden_size[0]))

    def dropout(self):
        pass

    @staticmethod
    @np.vectorize
    def sigmoid(activation):
        return 1 / (1 + math.e**-activation)

    @staticmethod
    @np.vectorize
    def dsigmoid(output):
        return output * (1 - output)

    @staticmethod
    @np.vectorize
    def error(target, output):
        return (target - output)**2

    @staticmethod
    @np.vectorize
    def derror(target, output):
        return 2 * (target - output)

    @staticmethod
    @np.vectorize
    def derrtodinput(target, output):
        return 0.5 * (target - output) * output * (1 - output)

    def feedf(self, input_data):
        if isinstance(input_data, list):
            input_data = np.array(input_data)
        if input_data.shape == self.input_layer.shape:
            self.input_layer = input_data
        else:
            return None

        iwdil = self.ih_weights.dot(self.input_layer)
        self.hidden_layers[0] = self.sigmoid(iwdil)

        for i in range(0, self.hidden_size[1]-1):
            hwdhl = self.hidden_weights[i].dot(self.hidden_layers[i])
            self.hidden_layers[i+1] = self.sigmoid(hwdhl)

        hodhl = self.ho_weights.dot(self.hidden_layers[-1])
        self.output_layer = self.sigmoid(hodhl)

        return self.output_layer

    def backp(self, t, lr):
        for n in range(0, self.hidden_size[0]-1):
            self.ho_weights[n] -= self.derrtodinput(t, self.output_layer) * lr
        # loop backwards through each hidden layer
        for n in range(self.hidden_size[1]-1, 1, -1):
            hl = self.hidden_layers[n]
            self.hidden_weights[n-1] -= self.derrtodinput(t, hl) * lr

    def train(self, data_set, learning_rate, iterations):
        for _ in range(iterations):
            for inp, expected_output in data_set:
                self.feedf(inp)
                self.backp(expected_output, learning_rate)

    def __repr__(self):
        s = (f'Input Layer:\n{self.input_layer}\n'
             f'Input-Hidden Weights:\n{self.ih_weights}\n'
             f'Hidden Layers:\n{self.hidden_layers}\n'
             f'Hidden Weights:\n{self.hidden_weights}\n'
             f'HiddenN-Output Weights:\n{self.ho_weights}\n'
             f'Output Layer:\n{self.output_layer}\n')
        return s


class Net(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.net = Net

    @commands.command()
    async def solve(self, ctx, equation: str):
        print(equation)
        ctx.send(f'```{equation}```')


def setup(bot):
    bot.add_cog(Net(bot))


if __name__ == '__main__':
    xor_set = [([0.0, 1.0], 1.0),
               ([1.0, 0.0], 1.0),
               ([1.0, 1.0], 0.0),
               ([0.0, 0.0], 0.0)]

    n = Network(2, (6, 4), 1)
    print(n)

    n.train(xor_set, 0.05, 100)

    for inp, out in xor_set:
        print(n.feedf(np.array(inp)), out)
