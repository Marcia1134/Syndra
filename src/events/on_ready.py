from discord.ext import commands
import logging

# Set Variables
logger = logging.getLogger('syndra')

class OnReady(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logger.info(f'{self.bot.user} has connected to Discord!')

        await self.bot.tree.sync() # Sync Tree

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OnReady(bot))

# Path: src/events/on_ready.py