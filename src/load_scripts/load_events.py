from discord.ext.commands import Bot
import os
import logging

# Set Variables
logger = logging.getLogger('syndra')

async def main(bot : Bot) -> None:
    logger.info('Loading events...')
    ignore = ['load_events.py', '__init__.py', '__pycache__'] # Files to ignore
    folder_path = './src/events'

    files = os.listdir(folder_path) # Get all files in the folder

    message = 'Loading Events:'
    for file in files:
        message += f'    - {file}'
    logger.debug(message)

    for cog in files:
        logger.debug(f"Filtering Cog: {cog}")
        if cog in ignore: # Ignore the files in the ignore list
            logger.debug(f"Ignoring {cog}")
            continue
        try:
            logger.debug(f'Loading {cog}')
            await bot.load_extension(f'events.{cog[:-3]}') # Load the cog
            logger.info(f'Loaded {cog}')
        except Exception as e:
            logger.error(f'Failed to load {cog}\n{e}')

# Path: src/events/load_events.py