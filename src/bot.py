from discord.ext.commands import Bot
from discord import Intents
from os import getenv 
from dotenv import load_dotenv
from cogs import load_cogs
from events import load_events
from asyncio import run
import sys
import pip
import ease

load_dotenv('config.env')

def main() -> None:
    bot = Bot(intents=Intents.all(), command_prefix=getenv("_")) # Create Bot

    bot.verbose = False
    if getenv("VERBOSE") == "True":
        bot.verbose = True
        print('Verbose Mode: ON')
    else:
        print('Verbose Mode: OFF')

    bot.version = "0.1.BETA"

    if bot.verbose:
        print(f'Version: {bot.version}')
        print(f'Python Version: {sys.version}')
        print(f'PIP Version: {pip.__version__}')
        print('Discord.py Version: {}'.format(pip.get_installed_distributions()[0].version))

    ease.print_line()

    if bot.verbose == False:
        print('Checking environment variables...')
    run(load_cogs.main(bot)) # Load Cogs
    run(load_events.main(bot)) # Load Events

    ease.print_line()

    bot.run(getenv("TOKEN"))

# Path: src/bot.py