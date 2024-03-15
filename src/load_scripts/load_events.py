from discord.ext.commands import Bot
import os

async def main(bot : Bot) -> None:
    if bot.verbose:
        print('Loading events...')
    ignore = ['load_events.py', '__init__.py', '__pycache__'] # Files to ignore
    folder_path = './src/events'

    files = os.listdir(folder_path) # Get all files in the folder

    if bot.verbose:
        print('Event Files:')
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
            await bot.load_extension(f'events.{cog[:-3]}') # Load the cog
            print(f'Loaded {cog}')
        except Exception as e:
            print(f'Failed to load {cog}\n{e}')

# Path: src/events/load_events.py