from discord import app_commands, Interaction
from discord.ext import commands
from database import tables

class BalanceCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="wallet", description="Check your balance")
    async def balance(self, interaction : Interaction, list_all : bool = False) -> None:
        # Check if the user has a balance entry
        wallet = tables.Wallet.get_or_none(id=interaction.user.id, server=interaction.guild_id)
        if wallet is None:
            wallet = tables.Wallet.create(id=interaction.user.id, server=interaction.guild_id, currency=tables.Currency.select().where(tables.Currency.server == interaction.guild_id).get(), balance=0)
            return

        # Check if the user wants to list all wallets
        if list_all:
            # Check if the user has a wallet entry
            wallets = tables.Wallet.select().where(tables.Wallet.id == interaction.user.id)
            if wallets.count() == 0:
                await interaction.response.send_message("You don't have a wallet entry")
                return

            # Send a response message with the user's wallets
            message = "Your wallets are:\n"
            for wallet in wallets:
                if self.bot.verbose:
                    print(f"Wallet: {wallet.id} {wallet.server} {wallet.currency} {wallet.balance}")
                message += f"{tables.Currency.select().where(tables.Currency.server == wallet.server).get().name} : {tables.Currency.select().where(tables.Currency.id == wallet.currency).get().symbol} {wallet.balance}\n"
            await interaction.response.send_message(message)
        else:
            # Send a response message with the user's wallet
            if self.bot.verbose:
                print(f"Wallet: {wallet.id} {wallet.server} {wallet.currency} {wallet.balance}")
            await interaction.response.send_message(f"Your balance is {tables.Currency.select().where(tables.Currency.id == wallet.currency).get().symbol} {wallet.balance}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BalanceCommand(bot))