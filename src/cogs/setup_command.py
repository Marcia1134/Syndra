import discord
from discord import app_commands
from discord.ext import commands

class SetupCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="setup", description="Setup the bot")
    async def setup(self, interaction : discord.Interaction) -> None:
        await interaction.response.send_message("Setup")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SetupCommand(bot))