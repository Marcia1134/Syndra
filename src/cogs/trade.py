import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from database.tables import Wallet, Product, Mail, Transaction, Currency, Server

load_dotenv('config.env')

verbose = False
if getenv("DEBUG") == "True":
    verbose = True

class TradeCommand(commands.Cog):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="trade", description="Create a trade request.")
    async def trade_request(self, interaction: discord.Interaction, reciever: discord.User, amount : int):
        
        # Fetch currency 
        try:
            currency = Currency.get(Currency.server == interaction.guild.id)
        except:
            await interaction.response.send_message("Currency not set.")
            return

        print("pass 1")

        # check if the currency exists
        try:
            Currency.get(Currency.id == currency.id)
        except:
            await interaction.response.send_message(f"Currency {currency} doesn't exist.")
            return
        
        print("pass 2")

        # fetch interactor's wallet
        try:
            wallet = Wallet.get(Wallet.id == interaction.user.id, Wallet.currency_id == currency)
        except:
            await interaction.response.send_message("You don't have a wallet.")
            return
        
        print("pass 3")

        # fetch reciever's wallet
        try:
            reciever_wallet = Wallet.get(Wallet.id == reciever.id, Wallet.currency_id == currency)
        except:
            # create wallet if it doesn't exist
            reciever_wallet = Wallet.create(id=reciever.id, server=interaction.guild_id, currency_id=currency, balance=0)
            return
        
        print("pass 4")

        # check if the interactor has enough money
        if wallet.balance < amount:
            await interaction.response.send_message("You don't have enough money.")
            return
        
        print("pass 5")

        # complete the trade
        wallet.balance -= amount
        reciever_wallet.balance += amount
        wallet.save()
        reciever_wallet.save()

        print('pass 6')

        # send verifcation (+ ping both parties)
        await interaction.response.send_message(f"Trade completed. {reciever.mention} has recieved {amount} {currency.name}.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TradeCommand(bot))