import discord
from discord import ui
from discord.ext import commands
from server_setup import FACE1

class RPView(ui.View):
    def __init__(self, bot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(label="Back", custom_id="back")
    async def back(self, interaction: discord.Interaction, button: ui.Button) -> None:
        # Go back to the main setup view
        await interaction.response.edit_message(view=FACE1.SetupView(self.bot), embed=FACE1.SetupEmbed(self.bot))
        if self.bot.verbose:
            print(f"Initalizing FACE1 for Server Setup in server {interaction.guild_id}")

class RPEmbed(discord.Embed):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = bot

        super().__init__(type="rich")

        self.title = "Role Pay Setup"
        self.description = "You need to use commands to set up Role Pay for your server"

        self.add_field(name="Adding an entry", value="Use the command `/rp add <role> <amount>` to add a new role pay entry")
        self.add_field(name="Removing an entry", value="Use the command `/rp remove <role>` to remove a role pay entry")
        self.add_field(name="Listing all entries", value="Use the command `/rp list` to list all role pay entries")
        self.add_field(name="Editing an entry", value="Use the command `/rp edit <role> <amount>` to edit a role pay entry")
        self.add_field(name="Paying all roles", value="Use the command `/rp pay` to pay all roles")