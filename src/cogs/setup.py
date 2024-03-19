import discord
from discord import app_commands
from discord.ext import commands
from database.tables import Server
from setup_app_data import first_time, base1
import logging

# Set Variables
logger = logging.getLogger('syndra')

class SetupCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="setup", description="Setup your server")
    async def setup(self, interaction : discord.Interaction) -> None:
        '''
        func : setup
        args : interaction : discord.Interaction
        ret  : None

        purpose:
            This function will setup the server for the first time. And act like a settings page for the server.

        args:
            interaction : discord.Interaction : The interaction object from the discord.py library.

        ret:
            None
        '''

        # Check for admin permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send("You don't have the required permissions")
            return

        # Check for existing setup
        server = Server.get_or_none(Server.id == interaction.guild.id)
        if server:
            # Send the settings page
            embed, view = base1.base1(bot=self.bot)
            await interaction.response.send_message(embed=embed, view=view)
        else:
            # Send the first time setup
            class testview(discord.ui.View):
                '''
                class : testview
                args : bot : commands.bot

                purpose:
                    This class will create a view for the setup command.

                struct :
                    __init__
                    Button : setup

                args:
                    None

                ret:
                    None
                '''
                def __init__(self, bot : commands.bot):
                    super().__init__(timeout=None)
                    self.bot = bot

                @discord.ui.button(label="Setup", style=discord.ButtonStyle.primary)
                async def setup(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                    # Send currency selection modal
                    await interaction.response.send_modal(first_time.modal(self.bot))

            # Send the first time setup
            await interaction.response.send_message("""1. Select Commands to restrict access to what your currency uses. \n2. Add Roles and their allowances /rp [role] [allowance].\n3. Select Role restrict access your Roles have.""", view=testview(self.bot))

            # Create the channels

            # channel overwrites for the command channel
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

            # channel overwrites for the annoucments channels
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

            # Create the category and channels
            cat = await interaction.guild.create_category("Syndra")
            await interaction.guild.create_text_channel("commands", overwrites=command_overwrites, category=cat)
            await interaction.guild.create_text_channel("trade", overwrites=speachless_overwrites, category=cat)
            await interaction.guild.create_text_channel("purchase", overwrites=speachless_overwrites, category=cat)
            await interaction.guild.create_text_channel("shop", overwrites=speachless_overwrites, category=cat)

            logger.debug(f"Created the channels for {interaction.guild.name}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SetupCommand(bot))

# Path: src/cogs/setup_command.py