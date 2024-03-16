from discord.ext.commands import Command
from database.tables import Commands, CommandConfig
from typing import List

ingore = ['setup', 'wallet', 'rp']

def main(commands : List[Command]) -> None:
    for command in commands:
        if command.name in ingore:
            continue
        if not Commands.select().where(Commands.command_name == command.name).exists():
            Commands.create(command_name=command.name)
    '''for command in Commands.select():
        if command.command_name not in [c.name for c in commands]:
            command.delete_instance()'''
    print("Commands added to database")