import discord
from discord import ui
from discord.ext import commands
from server_setup import ROLEPAY
from database import tables

# Define a custom modal for currency setup
class CurrencyModal(ui.Modal):
    def __init__(self, bot) -> None:
        super().__init__(timeout=None, title="Currency Setup")
        self.bot = bot

        # Create text input fields for currency name and symbol
        self.Curr_Name = ui.TextInput(label="Currency Name", placeholder="USD", custom_id="currency_name", required=True, min_length=3, max_length=10, style=discord.TextStyle.short)
        self.Curr_Symbol = ui.TextInput(label="Currency Symbol", placeholder="$", custom_id="currency_symbol", required=True, min_length=1, max_length=5, style=discord.TextStyle.short)

        # Add the text input fields to the modal
        self.add_item(self.Curr_Name)
        self.add_item(self.Curr_Symbol)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        # Retrieve the values entered by the user
        currency_name = self.Curr_Name.value
        currency_symbol = self.Curr_Symbol.value
        
        # Create a new server entry in the database if it doesn't exist
        tables.Server.create(id=interaction.guild_id)
        if self.bot.verbose:
            print(f"Server {interaction.guild_id} has been initialized")

        # Create a new currency entry in the database
        tables.Currency.create(server=tables.Server.get_by_id(interaction.guild_id), name=currency_name, symbol=currency_symbol)
        if self.bot.verbose:
            print(f"Currency {currency_name} has been added to server {interaction.guild_id}")

        # Send a response message with the entered currency details
        await interaction.response.send_message(f"Currency Name: {currency_name}\nCurrency Symbol: {currency_symbol}", ephemeral=True)

        if not self.bot.verbose:
            print(f"Currency {currency_name} has been added to server {interaction.guild_id}")

# Define a custom view for server setup
class SetupView(ui.View):
    def __init__(self, bot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(label="Currency Setup", custom_id="setup")
    async def setup(self, interaction: discord.Interaction, button: ui.Button) -> None:
        # Check if the server has already been set up
        server = tables.Server.get_or_none(id=str(interaction.guild_id))
        if server is not None:
            await interaction.response.send_message("This Server has already been set up. You may use the /manageserver command!", ephemeral=True)
            return

        # Open the currency setup modal
        await interaction.response.send_modal(CurrencyModal(self.bot))
        if self.bot.verbose:
            print(f"Currency Modal initialized for server {interaction.guild_id}")

# Define a custom embed for server setup
class SetupEmbed(discord.Embed):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = bot

        super().__init__()

        self.title = "Setup"
        self.description = "Setup your server"

        self.set_footer(text=f"Syndra Version {bot.version}")

        self.add_field(name="Currency", value="Set the Currency for your Server! \n\nYou will need to set the Currency Name and Symbol! (eg. USD, $)", inline=False)

        self.add_field(name="Role Pay", value="Set Role Pay.. Click the button to learn more!", inline=False)