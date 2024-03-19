from discord.utils import setup_logging
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
import logging

# Set Variables
logger = logging.getLogger('syndra')

load_dotenv('config.env')

def main() -> None:
    bot : Bot = Bot(intents=Intents.all(), command_prefix=getenv("_")) # Create Bot

    bot.verbose = False

    bot.version = "0.1.1.1"

    if bot.verbose:
        logger.info(f'Version: {bot.version}')
        logger.info(f'Python Version: {sys.version}')
        logger.info(f'PIP Version: {pip.__version__}')

    print_line()

    if bot.verbose == False:
        logging.info('Checking environment variables...')
    run(load_cogs.main(bot)) # Load Cogs
    run(load_events.main(bot)) # Load Events
    run(load_groups.main(bot)) # Reload Cogs

    checks.commands(bot.tree._get_all_commands())

    print_line()

    bot.run(getenv("TOKEN"))

    

# Path: src/bot.py