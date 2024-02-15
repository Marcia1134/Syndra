from discord.ext.commands import Bot
from discord import Intents
from os import getenv
from dotenv import load_dotenv
from cogs import load_cogs
from asyncio import run

load_dotenv()

def main() -> None:
    bot = Bot(intents=Intents.all(), command_prefix=getenv("_")) # Create Bot
    
    run(load_cogs.main(bot)) # Load Cogs

    bot.run(getenv("DISCORD_TOKEN"))

# Path: src/bot.py