import discord
from discord import app_commands
from discord.ext import commands
from database.tables import Server, CommandConfig, Commands
from checks.check_db_commands import ingore as ingore_list
from typing import List
import logging

# Set Variables
logger = logging.getLogger('syndra')

def commands1(commands : List) -> discord.ui.View:
    '''
    func : commands1
    args : commands : List
    ret  : discord.ui.View

    purpose:
        This function will take a list of commands and return a view for the setup command.

    args:
        commands : List : A list of commands to compare to the database.
        // Command (List[Command]) : Discord.ext.commands.Command : A command object from the discord.py library.

    ret:
        discord.ui.View : A view object from the discord.py library.
    '''
    class CommandSelection(discord.ui.View):
        '''
        class : CommandSelection
        args : commands : List[discord.ext.commands.Command]

        purpose:
            This class will create a view for the setup command.

        struct :
            __init__
            ?Select : discord.ui.Select
            interaction_check

        args:
            commands : List[discord.ext.commands.Command] : A list of commands to compare to the database.
            // Command (List[Command]) : Discord.ext.commands.Command : A command object from the discord.py library.

        ret:
            None
        '''
        def __init__(self, commands : List[discord.ext.commands.Command]) -> None:
            super().__init__(timeout=None)
            self.commands = commands
            options = []  # Create an empty list to store the select options
            for command in commands:  # Iterate over each command in the provided list
                if command.name in ingore_list:  # Check if the command name is in the ignore list
                    continue  # If it is, skip to the next iteration
                options.append(discord.SelectOption(label=command.name, value=command.name))  # Create a SelectOption object with the command name as both the label and value, and add it to the options list

            self.select = discord.ui.Select(placeholder="Select your commands", options=options)  # Create a Select object with the provided placeholder and options

            self.add_item(self.select)  # Add the Select object to the view

        class MyClass:
            async def interaction_check(self, interaction: discord.Interaction):
                '''
                method : interaction_check
                args : interaction : discord.Interaction

                purpose:
                    This method is called when an interaction occurs with the view.
                    It updates the database based on the selected commands.

                args:
                    interaction : discord.Interaction : The interaction object representing the user's interaction.

                ret:
                    None
                '''
                # Get the list of all commands from the database
                list_of_commands = Commands.select().execute()

                # Iterate over the selected commands from the interaction
                for command in list(interaction.data.values())[0]:
                    if command in ingore_list:
                        continue

                    # Check if the command already exists in the CommandConfig table
                    if CommandConfig.select().where(CommandConfig.command == command).exists():
                        # If the command exists, update its enabled status to True
                        CommandConfig.update(enabled=True).where(CommandConfig.command == command).execute()
                    else:
                        # If the command doesn't exist, create a new entry in the CommandConfig table with enabled status as True
                        CommandConfig.create(server=Server.get(interaction.guild_id), command=command, enabled=True)

                # Iterate over all commands in the database
                for command in list_of_commands:
                    # If a command is not present in the selected commands from the interaction, update its enabled status to False
                    if command.command_name not in [command for command in list(interaction.data.values())[0]]:
                        CommandConfig.update(enabled=False).where(CommandConfig.command == command.command).execute()

                # Send a response message to the user indicating that the commands have been updated
                await interaction.response.send_message("Commands have been updated", ephemeral=True, delete_after=5)

    return CommandSelection(commands)