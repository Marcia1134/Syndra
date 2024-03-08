import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from database.tables import Wallet, Product, Currency, Server

load_dotenv('config.env')

verbose = False
if getenv("DEBUG") == "True":
    verbose = True

async def create_product(wallet : Wallet.id) -> int:
    ...