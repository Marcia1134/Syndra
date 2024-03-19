from discord.ext.commands import Bot
import os
import logging

# Set Variables
logger = logging.getLogger('syndra')

async def main(bot : Bot, reload : bool = False) -> None:
    '''
    func : main
    args : bot : Bot
           reload : bool
    ret  : None

    purpose:
        This function will load all cogs in the cogs folder.

    args:
        bot : Bot : The discord.py bot object.
        reload : bool : If True, the cogs will be reloaded.

    ret:
        None
    '''
    logger.debug('Loading cogs...')
    ignore = ['load_cogs.py', '__init__.py', '__pycache__', 'chat.py'] # Files to ignore
    folder_path = './src/cogs'

    files = os.listdir(folder_path) # Get all files in the folder

    message = 'Loading Cogs:'
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
            if reload:
                await bot.reload_extension(f'cogs.{cog[:-3]}')
            else:
                await bot.load_extension(f'cogs.{cog[:-3]}') # Load the cog
            logger.info(f'Loaded {cog}')
        except Exception as e:
            logger.error(f'Failed to load {cog}\n{e}')
            if reload:
                try:
                    await bot.load_extension(f'cogs.{cog[:-3]}')
                except Exception as e:
                    logger.error(f'Failed to reload {cog}\n{e}')
                else:
                    logger.info(f'loaded {cog}')

# Path: src/cogs/load_cogs.py