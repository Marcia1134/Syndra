import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
import trade_app_data as trade

load_dotenv('config.env')

verbose = False
if getenv("DEBUG") == "True":
    verbose = True

class ProductCommandGroup(app_commands.Group):
    ...

async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(ProductCommandGroup(name="product", description="Product Commands"))