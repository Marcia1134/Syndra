from discord.ext.commands import Bot
import os

async def main(bot : Bot) -> None:
    ignore = ['load_events.py', '__init__.py', '__pycache__'] # Files to ignore
    folder_path = 'src/events'

    files = os.listdir(folder_path) # Get all files in the folder
    for cog in files:
        if cog in ignore: # Ignore the files in the ignore list
            break
        try:
            await bot.load_extension(f'events.{cog[:-3]}') # Load the cog
            print(f'Loaded {cog}')
        except Exception as e:
            print(f'Failed to load {cog}\n{e}')

# Path: src/events/load_events.py