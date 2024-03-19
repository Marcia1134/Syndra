import discord
from discord.ext import commands
from setup_app_data import commands1, role_perms1
from typing import Tuple
import logging

# Set Variables
logger = logging.getLogger('syndra')

def base1(bot : commands.Bot) -> Tuple[discord.Embed, discord.ui.View]:
    '''
    func : base1
    args : bot : commands.Bot
    ret  : Tuple[discord.Embed, discord.ui.View]

    purpose:
        This function will return the base setup guide.

    args:
        bot : commands.Bot : The bot object from the discord.py library.

    ret:
        Tuple[discord.Embed, discord.ui.View] : A tuple containing the embed and view.
        // discord.Embed : A embed object from the discord.py library.
        // discord.ui.View : A view object from the discord.py library.
    '''
    SetupGuideEmbed = discord.Embed(title="Setup Guide")
    SetupGuideEmbed.description = """
1. Select Commands to restrict access to what your currency uses.
2. Add Roles and their allowances /rp [role] [allowance].
3. Select Role restrict access your Roles have."""

    class SetupView(discord.ui.View):
        '''
        class : SetupView
        args : bot : commands.bot

        purpose:
            This class will create a view for the setup command.

        struct :
            __init__
            Button : commands
            Button : roles
        
        args:
            bot : commands.bot : The bot object from the discord.py library.

        ret:
            None
        '''
        def __init__(self, bot :commands.bot) -> None:
            super().__init__(timeout=None)
            self.bot = bot

        @discord.ui.button(label="commands", custom_id="commands")
        async def commands(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
            # pass off to the commands1 view
            await interaction.response.send_message("select commands", view=commands1.commands1(commands=self.bot.tree._get_all_commands()))

        @discord.ui.button(label="Roles", custom_id="roles")
        async def roles(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
            # pass off to the role_perms1 view
            embed, view = role_perms1.RolePerms1(interaction)
            await interaction.response.send_message(embed=embed, view=view)

    return SetupGuideEmbed, SetupView(bot=bot)