# About Mushishi ``v0.0.4``
Mushishi is a plugin-based bot focused on mimicking "human intelligence" with
features such as Factoids, Markov chains, and basic NLP.

### Requirements and Licensing
Mushishi was written with Python 3.6.1 and is licensed using the
[GNU aGPLv3](https://www.gnu.org/licenses/why-affero-gpl.html). It uses the
[discord.py](https://github.com/Rapptz/discord.py/tree/rewrite) API which is
licensed under the [MIT license](https://mit-license.org/). If available, it will utilize
[uvloop](https://github.com/MagicStack/uvloop)
for a speed boost to Python 3's `asyncio`.

## Current features:
Nothing important! Still being fleshed out.
* plugins
* basic admin functions
* basic utils functions
* basic reaction features

Check the TODO for a glance at future plans.

## Example usage: (w/ base plugins and server configuration)
    mu help

    mu help
    mu p ls

    mu plugin ld calc
    mu plot sin(x)
    mu plot sqrt(x)
    mu plot cos(x)/x**2

    mu p ld utils
    mu stats
    mu source

    mu p ld reaction
    mu reaction forward

# Installation
Clone the source to a local directory:

    git clone git@github.com:GRAYgoose124/mushishi.git
