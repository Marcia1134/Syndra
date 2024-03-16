import discord
from discord import app_commands
from discord.ext import commands
from database.tables import Server
from setup_app_data import first_time, base1

class SetupCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="setup", description="Setup your server")
    async def setup(self, interaction : discord.Interaction) -> None:

        # Check for admin permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send("You don't have the required permissions")
            return

        # Check for existing setup
        server = Server.get_or_none(Server.id == interaction.guild.id)
        if server:
            embed, view = base1.base1(bot=self.bot)
            await interaction.response.send_message(embed=embed, view=view)
        else:

            class testview(discord.ui.View):
                def __init__(self, bot : commands.bot):
                    super().__init__(timeout=None)
                    self.bot = bot

                @discord.ui.button(label="Setup", style=discord.ButtonStyle.primary)
                async def setup(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
                    # await interaction.response.send_message("Select your currency")
                    await interaction.response.send_modal(first_time.modal(self.bot))

            await interaction.response.send_message("test", view=testview(self.bot))

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

            cat = await interaction.guild.create_category("Syndra")
            await interaction.guild.create_text_channel("commands", overwrites=command_overwrites, category=cat)
            await interaction.guild.create_text_channel("trade", overwrites=speachless_overwrites, category=cat)
            await interaction.guild.create_text_channel("purchase", overwrites=speachless_overwrites, category=cat)
            await interaction.guild.create_text_channel("shop", overwrites=speachless_overwrites, category=cat)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SetupCommand(bot))

# Path: src/cogs/setup_command.py