from discord.ext.commands import Command
from database.tables import Server, Commands
from typing import List

def main(commands : List[Command]) -> None:
    for command in commands:
        if not Commands.select().where(Commands.command_name == command.name).exists():
            Commands.create(command_name=command.name)
    '''for command in Commands.select():
        if command.command_name not in [c.name for c in commands]:
            command.delete_instance()'''
    print("Commands added to database")