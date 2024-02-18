from discord import app_commands, Interaction
from discord.ext import commands
from database import tables

class BalanceCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="bal", description="Check your balance")
    async def balance(self, interaction : Interaction, list_all : bool = False) -> None:
        # Check if the user has a balance entry
        wallet = tables.Wallet.get_or_none(id=interaction.user.id, server=interaction.guild_id)
        if wallet is None:
            await interaction.response.send_message("You don't have a wallet entry", ephemeral=True)
            return

        # Check if the user wants to list all wallets
        if list_all:
            # Check if the user has a wallet entry
            wallets = tables.Wallet.select().where(tables.Wallet.id == interaction.user.id)
            if wallets.count() == 0:
                await interaction.response.send_message("You don't have a wallet entry", ephemeral=True)
                return

            # Send a response message with the user's wallets
            message = "Your wallets are:\n"
            for wallet in wallets:
                message += f"{tables.Currency.select().where(tables.Server.id == wallet.server).get().name}: {tables.Currency.select().where(tables.Currency.id == wallet.currency).get().symbol} {wallet.balance}\n"
            await interaction.response.send_message(message, ephemeral=True)
        else:
            # Send a response message with the user's wallet
            await interaction.response.send_message(f"Your balance is {tables.Currency.select().where(tables.Currency.id == wallet.currency).get().symbol} {wallet.balance}", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BalanceCommand(bot))