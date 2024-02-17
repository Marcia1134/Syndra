from discord import app_commands, Interaction
from discord.ext import commands

class ResyncCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="resync", description="Resync the server")
    async def resync(self, interaction : Interaction) -> None:
        await interaction.response.send_message("Resyncing Server...", ephemeral=True)
        await self.bot.tree.sync()
        print(f"Tree Resynced")
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ResyncCommand(bot))