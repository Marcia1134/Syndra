import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from database.tables import Wallet, Currency, CommandConfig, RoleCommandConfig

load_dotenv('config.env')

verbose = False
if getenv("DEBUG") == "True":
    verbose = True

class TradeCommand(commands.Cog):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="trade", description="Create a trade request.")
    async def trade_request(self, interaction: discord.Interaction, reciever: discord.User, amount : int):

        # Check if command is enabled in the server
        if not CommandConfig.get_or_none(server=interaction.guild_id, command=self.name).enabled:
            await interaction.response.send_message("Command is disabled in this server! To enable it, contact an admin.")
            return       
         
        # Check if the user is allowed to use the command (role)
        is_allowed = False
        for role in interaction.user.roles:
            if RoleCommandConfig.get_or_none(role=role.id, command=self.name) != None:
                is_allowed = True
                break

        if not is_allowed:
            await interaction.response.send_message("You are not allowed to use this command!")
            return

        # Fetch currency 
        try:
            currency = Currency.get(Currency.server == interaction.guild.id)
        except:
            await interaction.response.send_message("Currency not set.")
            return

        # check if the currency exists
        try:
            Currency.get(Currency.id == currency.id)
        except:
            await interaction.response.send_message(f"Currency {currency} doesn't exist.")
            return

        # fetch interactor's wallet
        try:
            wallet = Wallet.get(Wallet.id == interaction.user.id, Wallet.currency_id == currency)
        except:
            await interaction.response.send_message("You don't have a wallet.")
            return

        # fetch reciever's wallet
        try:
            reciever_wallet = Wallet.get(Wallet.id == reciever.id, Wallet.currency_id == currency)
        except:
            # create wallet if it doesn't exist
            reciever_wallet = Wallet.create(id=reciever.id, server=interaction.guild_id, currency_id=currency, balance=0)
            return
        
        # check if the interactor has enough money
        if wallet.balance < amount:
            await interaction.response.send_message("You don't have enough money.")
            return

        # complete the trade
        wallet.balance -= amount
        reciever_wallet.balance += amount
        wallet.save()
        reciever_wallet.save()

        # send verifcation (+ ping both parties)

        await interaction.response.send_message(f"**{amount} {currency.symbol}** has been sent to {reciever.mention}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TradeCommand(bot))