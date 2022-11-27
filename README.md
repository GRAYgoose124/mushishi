# About Mushishi ``v0.1.5``
Mushishi is a plugin-based bot with
features such as Factoids, Markov chains, and basic NLP.

## Current features:
* core plugins
    * basic admin functions
    * basic utils functions
    * basic reaction features
* featured plugins:
    * factoid 
    * calc (plotting requires a configured resource host.)
    * jukebox
    * see `src/mushishi/plugins` for undocumented plugins.

Check the TODO for a glance at future plans.

# Installation & Running
    # Clone the source to a local directory:
    > git clone git@github.com:GRAYgoose124/mushishi.git
    > cd mushishi
    > poetry shell  # Only if you want a virtual environment.

    > poetry install
    > mushi
## Docker
Container name: `mushishi`

    > docker-compose up [--build] -d

For the moment, docker support is supplementary, if you make developmental changes on mushishi, you need to use --build, (or docker --no-cache, docker-compose --force-build)

## Configuration
Follow `.env.template` for adding your key to the docker container. Otherwise, you can use the variable directly `VAR=TOKEN mushishi` or
run mushishi and update the token in `~/.config/mushishi/config.json`.

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

----

### Requirements and Licensing
Mushishi uses Python 3. It is licensed under
[GNU aGPLv3](https://www.gnu.org/licenses/why-affero-gpl.html). It uses the
[discord.py](https://github.com/Rapptz/discord.py/tree/rewrite) API which is
licensed under the [MIT license](https://mit-license.org/). If available, it will utilize
[uvloop](https://github.com/MagicStack/uvloop)
for a speed boost to Python 3's `asyncio`. (Windows only)