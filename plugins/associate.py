from discord.ext import commands
from discord.ext.commands import Cog

# from discord import Embed
# from collections import defaultdict, Counter
# from itertools import islice
# from nltk import pos_tag, CFG, Production
# from nltk import Nonterminal, nonterminals
# from nltk.corpus import brown
import json
from pathlib import Path
# import numpy as np
# import scipy
from matplotlib import pyplot as plt


# TODO: create a db graph of words ideas colloqialisms etc linked
# TODO: numpy arrays
# TODO: graph parser/traverser
# TODO graphvisualize
# category lists
# structural color texture

class CategoryWordGraph:
    def __init__(self, objectlist):
        self.objectlist = objectlist
        self.objects = {}  # {"object": (category, [("object1", weight1)])}
        self.auto_categories = {}  # {"category": [words]}

    def _obj_dist(self, o1, o2):
        pass

    def generate_graph(self):
        pass

    def associated_graph(self, object, depth):
        pass

    # Is obj of given type?
    def is_type_of(self, obj, template_object):
        super_type = obj
        while super_type in self.objects:
            super_type = self.is_a(super_type)
            if template_object == super_type:
                return True
        return None

    # What is the obj?
    def is_a(self, object):
        if object in self.objects:
            return self.objects[object][0]
        else:
            return None

    # What features characterize this object?
    def features(self, object):
        try:
            return self.objects[object][1]
        except KeyError:
            pass

    # What are the features of the parent objects?
    def super_features(self, object, depth=None):
        parent = object
        if depth is not None:
            i = 0
            while parent is not None and i < depth:
                features = []
                parent = self.is_a(parent)
                features.append(self.features(parent))
                i += 1
            return features
        else:
            return self.features(self.is_a(object))

    # What objects are in this category?
    def cat_objs(self, category):
        objects = []
        for object in self.objects.keys():
            if self.is_type_of(object, category):
                objects.append(object)

        return objects

    # Find the intersection of object features
    def shared_obj_features(self, obj1, obj2):
        return list(set(self.objects[obj1][1]) & set(self.objects[obj2][1]))

    # utilities
    def interactive_add_words(self):
        object = None

        # while wpt != "!q":
           #word phrase thought loop wpt | associations <-> , ; [,] : [:] ^
           # associations lead to different link types


        with open(self.objectlist, "w") as f:
            json.dump(self.objects, f)

    def definition_load(self):
        pass

    def sentence_load(self):
        pass

    def load_wordlist(self, jsonlist=None):
        if jsonlist is not None:
            self.objectlist = jsonlist

        with open(self.objectlist, "r") as f:
            self.objects = json.load(f)

    def save_wordlist(self, jsonlist=None):
        if jsonlist is not None:
            self.objectlist = jsonlist

        with open(self.objectlist, "w+") as f:
            json.dump(self.objects, f)


    def __repr__(self):
        return f'{self.objects}'


class WordGraph:
    def __init__(self):
        self.words = {}
        self.sents = []

    def add_word(self, tagged_word):
        # is the word in the graph?
        if tagged_word[0] in self.words:
            #
            if self.words[tagged_word] in self.words[tagged_word[0]]:
                pass
        else:
            self.words[tagged_word[0]] = {'pos': tagged_word[1], 'edges': []}

    def add_sentence(self, tagged_sentence):
        pass

    def give_contexts(self, word, contexts):
        pass


class WordGraphPod(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.graph = WordGraph()

    @commands.group(pass_context=True)
    async def wg(self, ctx):
        pass

    @wg.command()
    async def test(self, ctx, *sent: str):
        # sentence = ' '.join(sent)
        await ctx.send('')


class Associate(Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Associate(bot))
    bot.add_cog(WordGraphPod(bot))


if __name__ == '__main__':
    # Interactive writing loop
    parent_dir = Path(__file__).resolve().parent
    cwg = CategoryWordGraph(Path(parent_dir, "resources/data/words1.json"))
    #cwg.load_wordlist()
    cwg.interactive_add_words()

    for object in cwg.objects:
        print(f"A {object} is a {cwg.is_a(object)}")
        print(f"It has these features {cwg.features(object)}")

    cwg.save_wordlist()