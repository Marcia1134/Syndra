import discord
from discord import app_commands
from discord.ext import commands
from database.tables import Server, Currency, Commands, CommandConfig
from typing import List

def commands1(commands : List) -> discord.ui.View:
    class CommandSelection(discord.ui.View):
        def __init__(self, commands : List[discord.ext.commands.Command]) -> None:
            super().__init__(timeout=None)
            self.commands = commands
            
            options = []
            for command in commands:
                options.append(app_commands.ApplicationCommandOption(name=command.name, description="Enable or Disable this command", type=app_commands.ApplicationCommandOptionType.BOOLEAN, required=False))

            self.add_item(discord.ui.Select(placeholder="Select a command to enable or disable", options=options, custom_id="command_selection"))

        async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select) -> None:
            for option in select.options:
                if option.value == "true":
                    if not CommandConfig.select().where(CommandConfig.command_name == option.name).exists():
                        CommandConfig.create(server=Server.get(interaction.guild_id), command=option.name, enabled=True)
                    else:
                        CommandConfig.update(enabled=True).where(CommandConfig.server == interaction.guild_id, CommandConfig.command == option.name).execute()
                else:
                    if not CommandConfig.select().where(CommandConfig.command_name == option.name).exists():
                        CommandConfig.create(server=Server.get(interaction.guild_id), command=option.name, enabled=False)
                    else:
                        CommandConfig.update(enabled=False).where(CommandConfig.server == interaction.guild_id, CommandConfig.command == option.name).execute()

                interaction.response.send_message(f"{option.name} has been {'enabled' if option.value == 'true' else 'disabled'}")

    return CommandSelection(commands)