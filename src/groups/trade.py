import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv('config.env')

verbose = False
if getenv("DEBUG") == "True":
    verbose = True

class TradeCommandGroup(app_commands.Group):
    ...

async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(TradeCommandGroup(name="trade", description="Trading Commands"))