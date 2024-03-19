from discord.ext.commands import Bot
import os
import logging

# Set Variables
logger = logging.getLogger('syndra')

async def main(bot : Bot, reload : bool = False) -> None:
    logger.info('Loading groups...')
    ignore = ['load_groups.py', '__init__.py', '__pycache__'] # Files to ignore
    folder_path = './src/groups'

    files = os.listdir(folder_path) # Get all files in the folder

    message = 'Group Files:'
    for file in files:
        message += f'    - {file}'
    logger.debug(message)

    for group in files:
        logger.debug(f"Filtering group: {group}")
        if group in ignore: # Ignore the files in the ignore list
            logger.debug(f"Ignoring {group}")
            continue
        try:
            logger.debug(f'Loading {group}')
            if reload:
                await bot.reload_extension(f'groups.{group[:-3]}')
            else:
                await bot.load_extension(f'groups.{group[:-3]}') # Load the group
            logger.info(f'Loaded {group}')
        except Exception as e:
            logger.error(f'Failed to load {group}\n{e}')
            if reload:
                try:
                    await bot.load_extension(f'groups.{group[:-3]}')
                except Exception as e:
                    logger.error(f'Failed to reload {group}\n{e}')
                else:
                    logger.info(f'loaded {group}')

# Path: src/groups/load_groups.py