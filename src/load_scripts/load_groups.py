from discord.ext.commands import Bot
import os

async def main(bot : Bot, reload : bool = False) -> None:
    if bot.verbose:
        print('Loading groups...')
    ignore = ['load_groups.py', '__init__.py', '__pycache__'] # Files to ignore
    folder_path = '/home/marcia/Documents/GitHub/Syndra/src/groups'

    files = os.listdir(folder_path) # Get all files in the folder

    if bot.verbose:
        print('Group Files:')
        for file in files:
            print(f'    - {file}')

    for group in files:
        if bot.verbose:
            print(f"Filtering group: {group}")
        if group in ignore: # Ignore the files in the ignore list
            if bot.verbose:
                print(f"Ignoring {group}")
            continue
        try:
            if bot.verbose:
                print(f'Loading {group}')
            if reload:
                await bot.reload_extension(f'groups.{group[:-3]}')
            else:
                await bot.load_extension(f'groups.{group[:-3]}') # Load the group
            print(f'Loaded {group}')
        except Exception as e:
            print(f'Failed to load {group}\n{e}')
            if reload:
                try:
                    await bot.load_extension(f'groups.{group[:-3]}')
                except Exception as e:
                    print(f'Failed to reload {group}\n{e}')
                else:
                    print(f'loaded {group}')

# Path: src/groups/load_groups.py