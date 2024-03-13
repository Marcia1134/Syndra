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

class TradeCommandGroup(app_commands.Group):
    
    @app_commands.command(name="make", description="Create a trade request.")
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
            await interaction.response.send_message(f"{reciever.mention} doesn't have a wallet.")
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

    '''@app_commands.command(name="make", description="Create a trade request.")
    async def trade_request(self, interaction: discord.Interaction, reciever: discord.User, product_id: int):
        await trade.MTR(bot=self.bot, 
                  interaction=interaction, 
                  sender=interaction.author.id, 
                  reciever=reciever, 
                  product_id=product_id)'''
    
'''    @app_commands.command(name="view", description="List all of the requests made to you.")
    async def trade_view(self, interaction: discord.Interaction):
        await interaction.response.send_message("Trade [View] command used")
    
    @app_commands.command(name="accept", description="Accept a trade request.")
    async def trade_accept(self, interaction: discord.Interaction):
        await interaction.response.send_message("Trade [Accept] command used")

    @app_commands.command(name="decline", description="Decline a trade request.")
    async def trade_decline(self, interaction: discord.Interaction):
        await interaction.response.send_message("Trade [Decline] command used")

    @app_commands.command(name="cancel", description="Cancel a trade request.")
    async def trade_cancel(self, interaction: discord.Interaction):
        await interaction.response.send_message("Trade [Cancel] command used")

    @app_commands.command(name="status", description="Check the status of a trade request.")
    async def trade_status(self, interaction: discord.Interaction):
        await interaction.response.send_message("Trade [Status] command used")'''

async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(TradeCommandGroup(name="trade_request", description="Trading Commands"))