import discord
from discord import app_commands
from discord.ext import commands
from database.tables import Commands, RoleCommandConfig, RolePay, Server
from typing import Tuple, List

def RolePerms1(interaction : discord.Interaction) -> Tuple[discord.Embed, discord.ui.View]:
    
    RolePermsEmbed = discord.Embed(title="Role Permissions", description="Select the Role that should have access to the commands. Leave them blank if everyone should have access to that command. ")
    
    class RolePermsView(discord.ui.View):
        def __init__(self, interaction : discord.Interaction) -> None:
            super().__init__(timeout=None)
            self.interaction = interaction

            commands : List[RoleCommandConfig] = Commands.select().execute()
            roles_in_pay : List[RolePay] = RolePay.select().where(RolePay.server == self.interaction.guild_id).execute()
            for command in commands:
                options = []
                for role in roles_in_pay:
                    options.append(app_commands.ApplicationCommandOption(name=self.nteraction.guild.get_role(role.id).name, description="Enable or Disable this command", value=role.id, type=app_commands.ApplicationCommandOptionType.BOOLEAN, required=False))
                self.add_item(discord.ui.Select(placeholder=command.command_name, options=options, custom_id=command.command_name))

        async def on_select(self, interaction: discord.Interaction, select: discord.ui.Select) -> None:
            for option in select.options:
                if option.value == "true":
                    if not RoleCommandConfig.select().where(RoleCommandConfig.id == option.value, RoleCommandConfig.command == select.custom_id).exists():
                        RoleCommandConfig.create(role=option.value, command=select.custom_id)
                    else:
                        continue
                else:
                    if RoleCommandConfig.select().where(RoleCommandConfig.id == option.value, RoleCommandConfig.command == select.custom_id).exists():
                        RoleCommandConfig.delete().where(RoleCommandConfig.id == option.value, RoleCommandConfig.command == select.custom_id).execute()
                    else:
                        continue
            interaction.response.send_message(f"{option.name} has been {'enabled' if option.value == 'true' else 'disabled'}")

    return RolePermsEmbed, RolePermsView(interaction=interaction)