from discord import app_commands
from discord.ext import commands
from load_scripts import load_cogs

class ReloadCogs(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="reload_cogs", description="Reload all cogs")
    async def reload_cogs(self, interaction) -> None:
        await interaction.response.send_message("Reloading cogs...", ephemeral=True)

        await load_cogs.main(self.bot, reload=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ReloadCogs(bot))