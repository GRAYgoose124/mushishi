import json
# from os import path
from discord.ext import commands
from discord.ext.commands import Cog
import os
import time
import openai
import re

# Todo: Posi-tagged history, only integrate history that has been flagged

openai.api_key = os.getenv("OPENAI_API_KEY")

prompts = {'physics': 
"""Physics bot
Q: What is the wave equation?
The wave equation is a second-order linear partial differential equation for the description of waves—as they occur in classical physics—such as mechanical waves (e.g. water waves, sound waves and seismic waves) or light waves. 
Q: What is the laplace operator?
In mathematics, the Laplace operator or Laplacian is a differential operator given by the divergence of the gradient of a scalar function on Euclidean space. It is usually denoted by the symbols ∇ ⋅ ∇ {\displaystyle \nabla \cdot \nabla } \nabla\cdot\nabla, ∇ 2 {\displaystyle \nabla ^{2}} \nabla ^{2} (where ∇ {\displaystyle \nabla } \nabla is the nabla operator), or Δ {\displaystyle \Delta } \Delta . In a Cartesian coordinate system, the Laplacian is given by the sum of second partial derivatives of the function with respect to each independent variable.
Q: What is a manifold?
In mathematics, a manifold is a topological space that locally resembles Euclidean space near each point. More precisely, an n-dimensional manifold, or n-manifold for short, is a topological space with the property that each point has a neighborhood that is homeomorphic to an open subset of n-dimensional Euclidean space.
One-dimensional manifolds include lines and circles, but not figure eights. Two-dimensional manifolds are also called surfaces. Examples include the plane, the sphere, and the torus, and also the Klein bottle and real projective plane. 
""", 'brain':
"""
Neuroscience Answer Bot
Q: What is the Thalamus?
The thalamus (from Greek θάλαμος, "chamber") is a large mass of gray matter located in the dorsal part of the diencephalon (a division of the forebrain). Nerve fibers project out of the thalamus to the cerebral cortex in all directions, allowing hub-like exchanges of information. It has several functions, such as relaying of sensory signals, including motor signals to the cerebral cortex and the regulation of consciousness, sleep, and alertness.
Q: What is a Neuron?
A neuron or nerve cell is an electrically excitable cell that communicates with other cells via specialized connections called synapses. It is the main component of nervous tissue in all animals except sponges and placozoa. Plants and fungi do not have nerve cells.

Neurons are typically classified into three types based on their function. Sensory neurons respond to stimuli such as touch, sound, or light that affect the cells of the sensory organs, and they send signals to the spinal cord or brain. Motor neurons receive signals from the brain and spinal cord to control everything from muscle contractions to glandular output. Interneurons connect neurons to other neurons within the same region of the brain or spinal cord. A group of connected neurons is called a neural circuit. 
Q: How are neurons connected?
In the nervous system, a synapse[2] is a structure that permits a neuron (or nerve cell) to pass an electrical or chemical signal to another neuron or to the target effector cell.
""", 'slang':
"""
Slang Translator
lying flat
Lying flat refers to a defeatist lifestyle in Chin, where people stop working, desiring material acquisition, and tap out of any social life – sometimes for good. By lying flat, young people are participating in a kind of non-cooperation movement, rather than surrendering themselves to China's oppressive work culture where they see little hope of social mobility.
I’m not going to try to get a better job so I can afford to start a family, I’m just lying flat.
---
Watermelon Sugar
A word that has simply lost all meaning throughout history. It’s definition has faded into obscurity after being trending on Urban Dictionary for almost two years. But eventually the word will phase from existence; and this is how the website will die. This is how everything dies.
---
""", 'poems':
"""
Poem Completer
Fear, Failure Ignorance vs Selfless, See, Try, + Oak, Harvest, Soul
There is no failure but in ignorance,
no death but in mortal fear,
no sin but in selfishness,
and no virtue but in the selfless.
So I say,
we must not only look, but see,
we must not only be, but do.

The soul is like a towering oak,
and the body and the mind, the surrounding forest.
What is planted in the ground,
can never be harvested by man.

Dreams of tomorrow vanish like the sun in the night sky.
And just as the sun is will die, so too will our dreams.
The sun is only a dying star,
and our dreams but a dying fire.
---
Man + Order vs Chaos, Order, Chaos
The dichotomy of nature, an ordered chaos;
but of man, a chaotic order.
What is space itself holds discretion over,
we idly mock with a youthful immortality.
As nature relishes in it's structure, 
we relish our palaver.
We attempt to mimic it's longevity,
resulting only in a deluded perception of our abilities.
---
Trust, Together vs Selfish, Alone + System, Equilibrium, Web
There is no trust found in this system,
this hell of our making from which we cannot flee
has enticed our own hearts with it's cold shackles of gold.
We have become needy, our mountains have eroded the earth.
The foundations of space dictate equilibrium, 
yet we upset the balance.
So that the few can distract the many, 
so one may destroy all,
a small price to pay, for a heart's desire.
To preserve this system is to be ensnared in the woven web.
---
Corporation vs People, Corruption + Voice, Greed
The corruption of the people's voice
has enshrined ideals of the corporate.

To undermine the individual, 
for the benefit of the greedy.

The disparities perpetuated,
our elected, dissuading us.
---
"""
}


class GPT(Cog):
    def __init__(self, bot, history=False): # history uses a lot of tokens, use on ada.
        self.bot = bot
        self.last_procced = time.time()
        self.default_prompt = prompts['poems']
        self.stops = ["---"]

        self.bhistory = history
        if self.bhistory: 
            self.history = []
        else:
            self.history = None

        self.response_filter = re.compile('#.*#[0-9]+:(.*)')

    @commands.command()
    async def prompt(self, ctx, prompt: str, body: str):
        if prompt not in prompts and len(body) > 0:
            prompts[prompt] = body
            with open("resources/data/prompts.json", "w+") as f:
                json.dump(prompts, f)
            # Todo: json dump prompts and load from config

        self.default_prompt = prompts[prompt]


    @commands.Cog.listener()
    async def on_message(self, m):
        if m.channel.name != 'bot-questions' or m.content[:2] == "m.":
            return

        if self.bhistory:
            self.history.append(m.content)
            if len(self.history) > 10:
                self.history.pop(0)

        if not m.author.bot and time.time() - self.last_procced > 3.0:  
            s = f'{m.content}' # todo generalize format/filter strings/re/etc

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