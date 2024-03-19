from discord import app_commands, Interaction, Embed, ui, ButtonStyle
from discord.ext import commands
from database import tables
from typing import List
import logging

# Set Variables
logger = logging.getLogger('syndra')

class BalanceCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="wallet", description="Check your balance")
    async def balance(self, interaction : Interaction) -> None:
        '''
        func : balance
        args : interaction : Interaction
        ret  : None

        purpose:
            This function will check the balance of the user and return it to them.

        args:
            interaction : Interaction : The interaction object from the discord.py library.

        ret:
            None
        '''

        # Set the command name
        self.name = 'wallet'
        
        # Check if the user is allowed to use the command (role)
        is_allowed = False
        for role in interaction.user.roles:
            if tables.RoleCommandConfig.get_or_none(id=role.id, command=self.name) != None:
                is_allowed = True
                break

        if not is_allowed:
            await interaction.response.send_message("You are not allowed to use this command!")
            return

        # Check if the user has a balance entry
        wallet = tables.Wallet.get_or_none(id=interaction.user.id, server=interaction.guild_id)
        if wallet is None:
            wallet = tables.Wallet.create(id=interaction.user.id, server=interaction.guild_id, currency=tables.Currency.select().where(tables.Currency.server == interaction.guild_id).get(), balance=0)
            return

        def embed_builder(wallet):
            '''
            func : embed_builder
            args : wallet : tables.Wallet
            ret  : Embed

            purpose:
                This function will take a wallet object and return an embed object.

            args:
                wallet : tables.Wallet : A wallet object from the database.

            ret:
                Embed : A discord.Embed object.
            '''
            return Embed(title=f"{wallet.currency.name}", description=f"Your balance is {wallet.currency.symbol} {wallet.balance}")
        
        class FlipBook(ui.View):
            '''
            class : FlipBook
            args : ListOfWallets : list, server_id : int, user_id : int
            
            struc :
                [ui.View(timeout=None)]

                __init__
                Button : previous
                Button : next

            purpose:
                This is the flipbook view class for the balance command.

            args:
                ListOfWallets : list : A list of wallet objects from the database.
                server_id : int : The server id of the interaction.
                user_id : int : The user id of the interaction.

            ret:
                None
            '''
            def __init__(self, ListOfWallets : List[tables.Wallet], server_id : int, user_id : int):
                super().__init__(timeout=None)
                self.page = ListOfWallets.index(tables.Wallet.get(id=user_id, server=server_id)) # get the index of the wallet
                self.ListOfWallets = ListOfWallets

            @ui.button(label="previous", style=ButtonStyle.primary, emoji="⬅️")
            async def previous(self, interaction: Interaction, button: ui.Button):
                # if the page is 0, set it to the last page
                if self.page == 0:
                    self.page = len(self.ListOfWallets)
                self.page -= 1
                await interaction.response.edit_message(embed=embed_builder(self.ListOfWallets[self.page]))

            @ui.button(label="next", style=ButtonStyle.primary, emoji="➡️")
            async def next(self, interaction: Interaction, button: ui.Button):
                # if the page is the last page, set it to the first page
                if self.page == len(self.ListOfWallets) - 1:
                    self.page = -1
                self.page += 1
                await interaction.response.edit_message(embed=embed_builder(self.ListOfWallets[self.page]))

        # list of all the Wallets user has
        ListOfWallets = list(tables.Wallet.select().where(tables.Wallet.id == interaction.user.id).execute())

        logger.debug(f"user ({interaction.user.global_name}) has {len(ListOfWallets)} wallets.")

        # if the user only has one wallet, send the embed
        # if the user has more than one wallet, send the embed and the flipbook view
        if len(ListOfWallets) == 1:
            await interaction.response.send_message(embed=embed_builder(wallet))
        else:
            await interaction.response.send_message(embed=embed_builder(wallet), view=FlipBook(ListOfWallets, interaction.guild_id, interaction.user.id))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BalanceCommand(bot))