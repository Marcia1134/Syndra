import discord
from discord import app_commands
from discord.ext import commands
from database.tables import Wallet, Product, Currency, Server, ShopChannels

async def build_render(interaction):
    # Get the products
    products = Product.select().where(Product.owner.server == interaction.guild.id).execute()

    # Build Initial State

    # Inital Embed
    embed = discord.Embed(title="Shop", description="Welcome to the shop", color=0x00ff00)

    # Split
    


    # Add Products to Embed