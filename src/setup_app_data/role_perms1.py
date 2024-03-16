import discord
from discord import app_commands
from discord.ext import commands
from database.tables import Commands, RoleCommandConfig, RolePay, Server
from checks import check_db_commands
from typing import Tuple, List

def RolePerms1(interaction : discord.Interaction) -> Tuple[discord.Embed, discord.ui.View]:
    
    RolePermsEmbed = discord.Embed(title="Role Permissions", description="Select the Role that should have access to the commands. Leave them blank if everyone should have access to that command. ")
    
    class RolePermsView(discord.ui.View):
        def __init__(self, interaction : discord.Interaction) -> None:
            super().__init__(timeout=None)
            self.interaction = interaction

            commands : List[RoleCommandConfig] = Commands.select().execute()
            roles_in_pay : List[RolePay] = RolePay.select().where(RolePay.server == self.interaction.guild_id).execute()
            if not roles_in_pay:
                return None
            for command in commands:
                options = []
                for role in roles_in_pay:
                    options.append(discord.SelectOption(label=self.interaction.guild.get_role(role.role).name, value=role.role, description="Enable or Disable this command"))
                self.add_item(discord.ui.Select(placeholder=command.command_name, options=options, custom_id=command.command_name, min_values=0, max_values=len(roles_in_pay)))

        async def interaction_check(self, interaction: discord.Interaction):
            data = list(interaction.data.values()) # [List of selected], custom_id, ???
            print(data)
            
            roles_in_pay : List[RolePay] = RolePay.select().where(RolePay.server == self.interaction.guild_id).execute()

            if not data[0]:
                for role in roles_in_pay:
                    RoleCommandConfig.create(id=role.role, command=data[1])
                await interaction.response.send_message("Role Permissions have been updated", ephemeral=True, delete_after=5)
                return

            for role in roles_in_pay:
                if role.role not in data[0]:
                    RoleCommandConfig.delete().where(RoleCommandConfig.command == data[1] , RoleCommandConfig.id == role.role).execute()
            
            for role in data[0]:
                if RoleCommandConfig.select().where(RoleCommandConfig.command == data[1] , RoleCommandConfig.id == role).exists():
                    continue
                else:
                    RoleCommandConfig.create(id=role, command=data[1])

            for command in check_db_commands.ingore:
                print(command)
                for role in roles_in_pay:
                    print(role.role)
                    if not RoleCommandConfig.select().where(RoleCommandConfig.command == command, RoleCommandConfig.id == role.role).exists():
                        print("not exists, creating...")
                        RoleCommandConfig.create(id=role.role, command=command)
                    else:
                        print("exists, skipping...")
                        continue
                
            await interaction.response.send_message("Role Permissions have been updated", ephemeral=True, delete_after=5)

    embed, view = RolePermsEmbed, RolePermsView(interaction=interaction)
    
    if not view:
        interaction.response.send_message("No roles have been set up for this server. Please set up roles in the Pay command")
        return None, None
    
    return embed, view