import discord
from discord import app_commands
from discord.ext import commands
from database.tables import Server, Currency, CommandConfig, RoleCommandConfig
from setup_app_data import first_time, base1

class SetupCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="setup", description="Setup your server")
    async def setup(self, interaction : discord.Interaction) -> None:

        # Check if command is enabled in the server
        if not CommandConfig.get_or_none(server=interaction.guild_id, command=self.name).enabled:
            await interaction.response.send_message("Command is disabled in this server! To enable it, contact an admin.")
            return

        # Check if the user is allowed to use the command (role)
        is_allowed = False
        for role in interaction.user.roles:
            if RoleCommandConfig.get_or_none(role=role.id, command=self.name) != None:
                is_allowed = True
                break

        if not is_allowed:
            await interaction.response.send_message("You are not allowed to use this command!")
            return

        # Check for admin permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have the required permissions")
            return

        # Check for existing setup
        server = Server.get_or_none(Server.id == interaction.guild.id)
        if server:
            embed, view = base1.base1()
            await interaction.response.send_message(embed=embed, view=view)
        else:
            command_overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite( 
                    send_messages=True,
                    read_message_history=False
                ),
                interaction.guild.me: discord.PermissionOverwrite(
                    send_messages=True,
                    read_message_history=True,
                    manage_messages=True
                )
            }

            speachless_overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(
                    send_messages=False,
                    read_message_history=False
                ),
                interaction.guild.me: discord.PermissionOverwrite(
                    send_messages=True,
                    read_message_history=True,
                    manage_messages=True
                )
            }

            await interaction.guild.create_category("Syndra")
            await interaction.guild.create_text_channel("syndra-commands", overwrites=command_overwrites)
            await interaction.guild.create_text_channel("syndra-trade", overwrites=speachless_overwrites)
            await interaction.guild.create_text_channel("syndra-purchase", overwrites=speachless_overwrites)
            await interaction.guild.create_text_channel("syndra-shop", overwrites=speachless_overwrites)

            await interaction.response.send_modal(first_time.modal())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SetupCommand(bot))

# Path: src/cogs/setup_command.py