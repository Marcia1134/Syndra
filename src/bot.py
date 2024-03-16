from discord.ext.commands import Bot
from discord import Intents
from os import getenv 
from dotenv import load_dotenv
from load_scripts import load_cogs
from load_scripts import load_events
from load_scripts import load_groups
import checks
from asyncio import run
import sys
import pip
from ease import print_line

load_dotenv('config.env')

def main() -> None:
    bot : Bot = Bot(intents=Intents.all(), command_prefix=getenv("_")) # Create Bot

    bot.verbose = False
    if getenv("DEBUG") == "True":
        bot.verbose = True
        print('Verbose Mode: ON')
    else:
        print('Verbose Mode: OFF')

    bot.version = "0.1.1.1"

    if bot.verbose:
        print(f'Version: {bot.version}')
        print(f'Python Version: {sys.version}')
        print(f'PIP Version: {pip.__version__}')

    print_line()

    if bot.verbose == False:
        print('Checking environment variables...')
    run(load_cogs.main(bot)) # Load Cogs
    run(load_events.main(bot)) # Load Events
    run(load_groups.main(bot)) # Reload Cogs

    checks.commands(bot.tree._get_all_commands())

    for command in bot.tree._get_all_commands():
        print(f'{command.name}')

    print_line()

    bot.run(getenv("TOKEN"))

    

# Path: src/bot.py