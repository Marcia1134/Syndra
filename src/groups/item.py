import discord 
from discord import app_commands
from discord.ext import commands
from product_app_data import create

class ShopGroupCommand(app_commands.Group):

    @app_commands.command(name="create", description="Create a product")
    async def create_product(self, interaction : discord.Interaction) -> None:
        await create.create_product(interaction)

    @app_commands.command(name="delete", description="Delete a product")
    async def delete_product(self, interaction : discord.Interaction) -> None:
        await interaction.response.send_message("Delete Product")

    @app_commands.command(name="edit", description="Edit a product")
    async def edit_product(self, interaction : discord.Interaction) -> None:
        await interaction.response.send_message("Edit Product")

async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(ShopGroupCommand(name="item", description="Manage your items"))