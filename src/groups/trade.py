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

class TradeCommandGroup(app_commands.Group):
    
    @app_commands.command(name="make", description="Create a trade request.")
    async def trade_request(self, interaction: discord.Interaction, reciever: discord.User, product_id: int):
        await trade.MTR(bot=self.bot, 
                  interaction=interaction, 
                  sender=interaction.user, 
                  reciever=reciever, 
                  product_id=product_id)
    
    @app_commands.command(name="view", description="List all of the requests made to you.")
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
        await interaction.response.send_message("Trade [Status] command used")

async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(TradeCommandGroup(name="trade_request", description="Trading Commands"))