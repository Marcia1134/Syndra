import discord
from discord import app_commands
from discord.ext import commands
from database.tables import Server, CommandConfig, Commands
from checks.check_db_commands import ingore as ingore_list
from typing import List

def commands1(commands : List) -> discord.ui.View:
    class CommandSelection(discord.ui.View):
        def __init__(self, commands : List[discord.ext.commands.Command]) -> None:
            super().__init__(timeout=None)
            self.commands = commands
            options = []
            for command in commands:
                if command.name in ingore_list:
                    continue
                options.append(discord.SelectOption(label=command.name, value=command.name))

            self.select = discord.ui.Select(placeholder="Select your commands", options=options)

            self.add_item(self.select)

        async def interaction_check(self, interaction: discord.Interaction):
            list_of_commands = Commands.select().execute()
            for command in list(interaction.data.values())[0]:
                if command in ingore_list:
                    continue
                if CommandConfig.select().where(CommandConfig.command == command).exists():
                    CommandConfig.update(enabled=True).where(CommandConfig.command == command).execute()
                else:
                    CommandConfig.create(server=Server.get(interaction.guild_id),command=command, enabled=True)

            for command in list_of_commands:
                if command.command_name not in [command for command in list(interaction.data.values())[0]]:
                    CommandConfig.update(enabled=False).where(CommandConfig.command == command.command).execute()
                
            await interaction.response.send_message("Commands have been updated", ephemeral=True, delete_after=5)

    return CommandSelection(commands)