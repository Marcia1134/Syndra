import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from trade_app_data import make_trade_request

load_dotenv('config.env')

verbose = False
if getenv("DEBUG") == "True":
    verbose = True

async def MTR(bot : commands.bot, 
        interaction : discord.Interaction, 
        sender : discord.User, 
        reciever : discord.User, 
        product_id : int) -> int:
    
    return await make_trade_request.main(bot=bot, 
                                   interaction=interaction, 
                                   sender=sender, 
                                   reciever=reciever, 
                                   product_id=product_id)