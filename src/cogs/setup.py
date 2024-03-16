import discord
from discord import app_commands
from discord.ext import commands
from database.tables import Server, Currency, CommandConfig, RoleCommandConfig

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
            await interaction.response.send_message("Server already setup")
        else:
            ...

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SetupCommand(bot))

# Path: src/cogs/setup_command.py