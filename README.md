# About Mushishi ``v0.1.5``
Mushishi is a plugin-based bot with
features such as Factoids, Markov chains, and basic NLP.

### Requirements and Licensing
Mushishi uses Python 3. It is licensed under
[GNU aGPLv3](https://www.gnu.org/licenses/why-affero-gpl.html). It uses the
[discord.py](https://github.com/Rapptz/discord.py/tree/rewrite) API which is
licensed under the [MIT license](https://mit-license.org/). If available, it will utilize
[uvloop](https://github.com/MagicStack/uvloop)
for a speed boost to Python 3's `asyncio`. (Windows only)

## Current features:
* core plugins
    * basic admin functions
    * basic utils functions
    * basic reaction features
* feature plugins
    * factoid 
    * calc (plot needs resource host configured)
    * jukebox


Check the TODO for a glance at future plans.

# Installation & Running
    # Clone the source to a local directory:
    > git clone git@github.com:GRAYgoose124/mushishi.git
    > cd mushishi
    > poetry shell  # Only if you want a virtual environment.

    > poetry install
    > mushi
## Configuration
Run mushishi and check `~/.config/mushishi` for details.
## Resources
Any files to be be viewed need to be served by some resource host. The url to the can be set in the config, but the resource host is independently run.
## Example usage: (w/ base plugins and server configuration)
    mu help
    mu p ls

    mu p ld calc
    mu plot sin(x)
    mu plot sqrt(x)
    mu plot cos(x)/x**2

    # mu p ld utils
    mu stats
    mu source

    mu p ld reaction
    mu reaction forward

    m.p ld factoid
    m.fact add Hello World! >> Hi Human!

