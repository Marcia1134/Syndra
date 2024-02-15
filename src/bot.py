from discord.ext.commands import Bot
from discord import Intents
from os import getenv
from dotenv import load_dotenv
from cogs import load_cogs
from events import load_events
from asyncio import run

load_dotenv('.env')

def main() -> None:
    bot = Bot(intents=Intents.all(), command_prefix=getenv("_")) # Create Bot

    run(load_cogs.main(bot)) # Load Cogs
    run(load_events.main(bot)) # Load Events

    bot.run(getenv("TOKEN"))

# Path: src/bot.py