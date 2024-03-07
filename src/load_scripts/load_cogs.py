from discord.ext.commands import Bot
import os

async def main(bot : Bot, reload : bool = False) -> None:
    if bot.verbose:
        print('Loading cogs...')
    ignore = ['load_cogs.py', '__init__.py', '__pycache__'] # Files to ignore
    folder_path = '/home/marcie/Documents/GitHub/Syndra/src/cogs'

    files = os.listdir(folder_path) # Get all files in the folder

    if bot.verbose:
        print('Cog Files:')
        for file in files:
            print(f'    - {file}')

    for cog in files:
        if bot.verbose:
            print(f"Filtering Cog: {cog}")
        if cog in ignore: # Ignore the files in the ignore list
            if bot.verbose:
                print(f"Ignoring {cog}")
            continue
        try:
            if bot.verbose:
                print(f'Loading {cog}')
            if reload:
                await bot.reload_extension(f'cogs.{cog[:-3]}')
            else:
                await bot.load_extension(f'cogs.{cog[:-3]}') # Load the cog
            print(f'Loaded {cog}')
        except Exception as e:
            print(f'Failed to load {cog}\n{e}')
            if reload:
                try:
                    await bot.load_extension(f'cogs.{cog[:-3]}')
                except Exception as e:
                    print(f'Failed to reload {cog}\n{e}')
                else:
                    print(f'loaded {cog}')

# Path: src/cogs/load_cogs.py