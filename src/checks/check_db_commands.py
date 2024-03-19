from discord.ext.commands import Command
from database.tables import Commands
from typing import List
import logging
logger = logging.getLogger('syndra')

# List of ignored commands
ingore = ['setup', 'wallet', 'rp', 'chat']

def main(commands : List[Command]) -> None:
    '''
    func : main
    args : commands : List[Command]
    ret  : None

    purpose:
        This function will take a list of commands and compare them to the commands in the database.
        If the command is not in the database, it will be added.

    args:
        commands : List[Command] : A list of commands to compare to the database.
        // Command (List[Command]) : Discord.ext.commands.Command : A command object from the discord.py library.
    '''
    for command in commands:
    
        if command.name in ingore:
            logger.debug(f"Ignoring command: {command.name}")
            continue

        if not Commands.select().where(Commands.command_name == command.name).exists():
            logger.debug(f"Adding command: {command.name}")
            Commands.create(command_name=command.name)
    
    logger.info("Commands Added, Command Check Complete!")