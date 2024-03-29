import discord 
from discord import app_commands
from discord.ext import commands
from database.tables import Server, Currency
from setup_app_data import base1

def modal(bot : commands.bot) -> discord.ui.Modal:
    """
    Creates a modal for currency setup.

    Args:
        bot (commands.bot): The bot instance.

    Returns:
        discord.ui.Modal: The created modal.
    """
    class SetupModal(discord.ui.Modal):
        def __init__(self):
            super().__init__(timeout=None, title="Currency Setup")
            self.Curr_Name = discord.ui.TextInput(label="Currency Name", placeholder="USD", custom_id="currency_name", required=True, min_length=3, max_length=10, style=discord.TextStyle.short)
            self.Curr_Value = discord.ui.TextInput(label="Currency Value", placeholder="100%", custom_id="currency_value", required=True, min_length=1, max_length=3, style=discord.TextStyle.short)
            self.Curr_Symbol = discord.ui.TextInput(label="Currency Symbol", placeholder="$", custom_id="currency_symbol", required=True, min_length=1, max_length=5, style=discord.TextStyle.short)
            self.add_item(self.Curr_Name)
            self.add_item(self.Curr_Value)
            self.add_item(self.Curr_Symbol)

        async def on_submit(self, interaction: discord.Interaction) -> None:
            """
            Event handler for when the modal is submitted.

            Args:
                interaction (discord.Interaction): The interaction object.

            Returns:
                None
            """
            currency_name = self.Curr_Name.value
            currency_value = self.Curr_Value.value
            currency_symbol = self.Curr_Symbol.value
            Server.create(id=interaction.guild_id)
            Currency.create(server=Server.get_by_id(interaction.guild_id), name=currency_name, value=currency_value, symbol=currency_symbol)
            embed, view = base1.base1(bot=bot)
            await interaction.response.send_message(embed=embed, view=view)

    return SetupModal()