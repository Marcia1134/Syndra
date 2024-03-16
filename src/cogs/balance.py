from discord import app_commands, Interaction, Embed, ui, ButtonStyle
from discord.ext import commands
from database import tables

class BalanceCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="wallet", description="Check your balance")
    async def balance(self, interaction : Interaction) -> None:
        
        # Check if command is enabled in the server
        if not tables.CommandConfig.get_or_none(server=interaction.guild_id, command=self.name).enabled:
            await interaction.response.send_message("Command is disabled in this server! To enable it, contact an admin.")
            return

        # Check if the user has a balance entry
        wallet = tables.Wallet.get_or_none(id=interaction.user.id, server=interaction.guild_id)
        if wallet is None:
            wallet = tables.Wallet.create(id=interaction.user.id, server=interaction.guild_id, currency=tables.Currency.select().where(tables.Currency.server == interaction.guild_id).get(), balance=0)
            return

        def embed_builder(wallet):
            return Embed(title=f"{wallet.currency.name}", description=f"Your balance is {wallet.currency.symbol} {wallet.balance}")
        
        class FlipBook(ui.View):
            def __init__(self, ListOfWallets, server_id, user_id):
                super().__init__(timeout=None)
                self.page = ListOfWallets.index(tables.Wallet.get(id=user_id, server=server_id))
                self.ListOfWallets = ListOfWallets

            @ui.button(label="previous", style=ButtonStyle.primary, emoji="⬅️")
            async def previous(self, interaction: Interaction, button: ui.Button):
                if self.page == 0:
                    self.page = len(self.ListOfWallets)
                self.page -= 1
                await interaction.response.edit_message(embed=embed_builder(self.ListOfWallets[self.page]))

            @ui.button(label="next", style=ButtonStyle.primary, emoji="➡️")
            async def next(self, interaction: Interaction, button: ui.Button):
                if self.page == len(self.ListOfWallets) - 1:
                    self.page = -1
                self.page += 1
                await interaction.response.edit_message(embed=embed_builder(self.ListOfWallets[self.page]))

        # list of all currency interactor is connected to
        ListOfWallets = list(tables.Wallet.select().where(tables.Wallet.id == interaction.user.id).execute())

        print(ListOfWallets)

        if len(ListOfWallets) == 1:
            await interaction.response.send_message(embed=embed_builder(wallet))
        else:
            await interaction.response.send_message(embed=embed_builder(wallet), view=FlipBook(ListOfWallets, interaction.guild_id, interaction.user.id))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BalanceCommand(bot))