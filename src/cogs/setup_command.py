import discord
from discord import app_commands
from discord.ext import commands
from server_setup import FACE1

class SetupCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="setup", description="Setup your server")
    async def setup(self, interaction : discord.Interaction) -> None:
        if self.bot.verbose == True:
            print(f"Initalizing FACE1 for Server Setup in server {interaction.guild_id}")
        await interaction.response.send_message(view=FACE1.SetupView(self.bot), embed=FACE1.SetupEmbed(self.bot), ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SetupCommand(bot))

# Path: src/cogs/setup_command.py