import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
import trade_app_data as trade
import product_app_data as product

load_dotenv('config.env')

verbose = False
if getenv("DEBUG") == "True":
    verbose = True

class ProductCommandGroup(app_commands.Group):
    
    @app_commands.command(name="create", description="Create a new product")
    async def create_product_command(self, interaction: discord.Interaction) -> None:
        await product.create_product_func(interaction=interaction)
        return

async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(ProductCommandGroup(name="product", description="Product Commands"))