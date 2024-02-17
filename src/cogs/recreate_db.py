from discord import app_commands, Interaction
from discord.ext import commands
import database

class ReDBCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="redb", description="Recreate Database")
    async def redb(self, interaction : Interaction) -> None:
        await interaction.response.send_message("Deleteing all tables and recreating DB", ephemeral=True)
        database.recreate_db()
        print(f"Database Recreated")
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ReDBCommand(bot))