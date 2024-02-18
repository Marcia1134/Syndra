from discord import app_commands, Interaction, User
from discord.ext import commands
from database import tables
from trade_application_data.verification_sender import VerificationSender, VerificationSenderEmbed

class TradeCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="trade", description="Trade with another user")
    async def trade(self, interaction : Interaction, user : User, amount : int) -> None:
        
        # Check if amount is positive
        if amount <= 0:
            if self.bot.verbose:
                print("Amount must be positive")
            await interaction.response.send_message("Amount must be positive", ephemeral=True)
            return
        
        # Check if the sender has a wallet entry
        sender_wallet = tables.Wallet.get_or_none(id=interaction.user.id, server=interaction.guild_id)
        if sender_wallet is None:
            if self.bot.verbose:
                print("You don't have a wallet entry")
            await interaction.response.send_message("You don't have a wallet entry", ephemeral=True)
            return

        # Check if the receiver has a wallet entry
        reciever_wallet = tables.Wallet.get_or_none(id=user.id, server=interaction.guild_id)
        if reciever_wallet is None:
            if self.bot.verbose:
                print("The user doesn't have a wallet entry")
            await interaction.response.send_message("The user doesn't have a wallet entry", ephemeral=True)
            return

        # Check if the sender has enough balance
        if sender_wallet.balance < amount:
            if self.bot.verbose:
                print("You don't have enough balance")
            await interaction.response.send_message("You don't have enough balance", ephemeral=True)
            return

        # Send verification message to the sender
        await interaction.response.send_message(embed=VerificationSenderEmbed(interaction.user, amount, sender_wallet), view=VerificationSender(interaction.user, amount, interaction, sender_wallet, reciever_wallet))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TradeCommand(bot))