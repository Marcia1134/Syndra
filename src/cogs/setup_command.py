import discord
from discord import ui
from discord import app_commands
from discord.ext import commands

class SetupView(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @ui.button(label="Setup", style=discord.ButtonStyle.blurple, custom_id="setup")
    async def setup(self, interaction: discord.Interaction, button: ui.Button) -> None:
        await interaction.response.send_message("Setup your server")

class SetupEmbed(discord.Embed):
    def __init__(self, bot : commands.bot) -> None:
        self.bot = bot

        super().__init__()

        self.title = "Setup"
        self.description = "Setup your server"

        self.set_footer(text=f"Syndra Version {bot.version}")

        self.add_field(name="Prefix", value="Set the prefix for your server")
        self.add_field(name="Channel", value="Set the channel for your server")
        self.add_field(name="Role", value="Set the role for your server")

class SetupCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="setup", description="Setup your server")
    async def setup(self, interaction : discord.Interaction) -> None:
        await interaction.response.send_message(view=SetupView(), embed=SetupEmbed(self.bot), ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SetupCommand(bot))

# Path: src/cogs/setup_command.py