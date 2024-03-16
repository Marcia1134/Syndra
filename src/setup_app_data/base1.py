import discord
from discord import app_commands
from discord.ext import commands
from database.tables import Server, Currency
from setup_app_data import commands1, role_perms1
from typing import Tuple

def base1(bot : commands.Bot) -> Tuple[discord.Embed, discord.ui.View]:
    SetupGuideEmbed = discord.Embed(title="Setup Guide")
    SetupGuideEmbed.description = """
1. Select Commands to restrict access to what your currency uses.
2. Add Roles and their allowances /rp [role] [allowance].
3. Select Role restrict access your Roles have."""

    class SetupView(discord.ui.View):
        def __init__(self, bot :commands.bot) -> None:
            super().__init__(timeout=None)
            self.bot = bot

        @discord.ui.button(label="commands", custom_id="commands")
        async def commands(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
            await interaction.response.send_message("select commands", view=commands1.commands1(commands=self.bot.tree._get_all_commands()))

        @discord.ui.button(label="Roles", custom_id="roles")
        async def roles(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
            embed, view = role_perms1.RolePerms1(interaction)
            await interaction.response.send_message(embed=embed, view=view)

    return SetupGuideEmbed, SetupView(bot=bot)