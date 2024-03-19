import discord
from discord import app_commands
from discord.ext import commands
from database.tables import Commands, RoleCommandConfig, RolePay, Server
from checks import check_db_commands
from typing import Tuple, List
import logging

# Set Variables
logger = logging.getLogger('syndra')

def RolePerms1(interaction : discord.Interaction) -> Tuple[discord.Embed, discord.ui.View]:
    """
    Retrieves the role permissions for commands and returns an embed and view.

    Args:
        interaction (discord.Interaction): The interaction object representing the user's interaction with the bot.

    Returns:
        Tuple[discord.Embed, discord.ui.View]: A tuple containing the embed and view objects for the role permissions.

    Raises:
        None

    """
    RolePermsEmbed = discord.Embed(title="Role Permissions", description="Select the Role that should have access to the commands. Leave them blank if everyone should have access to that command. ")
    
    class RolePermsView(discord.ui.View):
        def __init__(self, interaction : discord.Interaction) -> None:
            """
            Initializes an instance of the RolePerms class.

            Args:
                interaction (discord.Interaction): The interaction object representing the user's interaction with the bot.

            Returns:
                None
            """
            super().__init__(timeout=None)
            self.interaction = interaction

            # Retrieve the list of RoleCommandConfig objects from the database
            commands : List[RoleCommandConfig] = Commands.select().execute()

            # Retrieve the list of RolePay objects for the server
            roles_in_pay : List[RolePay] = RolePay.select().where(RolePay.server == self.interaction.guild_id).execute()

            # If there are no roles in the RolePay table, return None
            if not roles_in_pay:
                return None

            # Iterate over each RoleCommandConfig object
            for command in commands:
                options = []

                # Iterate over each RolePay object
                for role in roles_in_pay:
                    # Create a SelectOption object for each role
                    options.append(discord.SelectOption(label=self.interaction.guild.get_role(role.role).name, value=role.role, description="Enable or Disable this command"))

                # Create a Select object with the options and add it to the UI
                self.add_item(discord.ui.Select(placeholder=command.command_name, options=options, custom_id=command.command_name, min_values=0, max_values=len(roles_in_pay)))

        async def interaction_check(self, interaction: discord.Interaction):
                    """
                    Check and update role permissions based on the user interaction.

                    Args:
                        interaction (discord.Interaction): The user interaction object.

                    Returns:
                        None
                    """
                    # Get the selected data from the user interaction
                    data = list(interaction.data.values())  # [List of selected], custom_id, ???
                    logger.debug(data)
                    
                    # Retrieve all RolePay objects for the server
                    roles_in_pay: List[RolePay] = RolePay.select().where(RolePay.server == self.interaction.guild_id).execute()

                    # If no roles are selected, assign the command to all roles in RolePay
                    if not data[0]:
                        for role in roles_in_pay:
                            RoleCommandConfig.create(id=role.role, command=data[1])
                        await interaction.response.send_message("Role Permissions have been updated", ephemeral=True, delete_after=5)
                        return

                    # Remove the command from roles that are not selected
                    for role in roles_in_pay:
                        if role.role not in data[0]:
                            RoleCommandConfig.delete().where(RoleCommandConfig.command == data[1], RoleCommandConfig.id == role.role).execute()
                        
                    # Add the command to roles that are selected and not already assigned
                    for role in data[0]:
                        if RoleCommandConfig.select().where(RoleCommandConfig.command == data[1], RoleCommandConfig.id == role).exists():
                            continue
                        else:
                            RoleCommandConfig.create(id=role, command=data[1])

                    # Add missing commands from check_db_commands.ignore to all roles in RolePay
                    for command in check_db_commands.ignore:
                        logger.debug(command)
                        for role in roles_in_pay:
                            logger.debug(role.role)
                            if not RoleCommandConfig.select().where(RoleCommandConfig.command == command, RoleCommandConfig.id == role.role).exists():
                                logger.debug("not exists, creating...")
                                RoleCommandConfig.create(id=role.role, command=command)
                            else:
                                logger.debug("exists, skipping...")
                                continue
                            
                    await interaction.response.send_message("Role Permissions have been updated", ephemeral=True, delete_after=5)

    embed, view = RolePermsEmbed, RolePermsView(interaction=interaction)
    
    if not view:
        interaction.response.send_message("No roles have been set up for this server. Please set up roles in the Pay command")
        logger.error("No roles have been set up for this server. Please set up roles in the Pay command")
        return None, None
    
    return embed, view