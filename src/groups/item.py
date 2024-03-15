import discord 
from discord import app_commands
from discord.ext import commands
from product_app_data import create
from database.tables import Product, Wallet

class ShopGroupCommand(app_commands.Group):

    @app_commands.command(name="create", description="Create an item")
    async def create_product(self, interaction : discord.Interaction) -> None:
        await create.create_product(interaction)

    @app_commands.command(name="delete", description="Delete an item")
    async def delete_product(self, interaction : discord.Interaction, item_id : int) -> None:
        # Check if the product exists
        product = Product.get_or_none(Product.id == item_id)
        if product is None:
            await interaction.response.send_message(f"Item with ID: {item_id} not found.")
            return
        
        # Check if the interactor is the owner of the product
        wallet = Wallet.get(Wallet.id == interaction.user.id)
        if product.owner != wallet:
            await interaction.response.send_message("You don't have the required permissions")
            return
        
        # Display Product Infomation
        embed = discord.Embed(title=f"{product.emoji} {product.name}", description=f"{product.description}")
        embed.add_field(name="Price", value=f"{product.price}")
        embed.add_field(name="Stock", value=f"{product.stock}", inline=False)
        embed.add_field(name="Is Active", value=f"{product.is_active}")
        
        # Confirmation View
        class DeleteProductView(discord.ui.View):
            def __init__(self, product):
                super().__init__()
                self.product = product

            @discord.ui.button(label="Yes", style=discord.ButtonStyle.primary, emoji="✅")
            async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
                product.delete_instance()
                await interaction.response.send_message("Item Deleted")
                self.stop()

            @discord.ui.button(label="No", style=discord.ButtonStyle.primary, emoji="❌")
            async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_message("Item Not Deleted")
                self.stop()
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="edit", description="Edit an item")
    async def edit_product(self, interaction : discord.Interaction, item_id : int) -> None:
        # Check if the product exists
        product = Product.get_or_none(item_id)
        if product is None:
            await interaction.response.send_message(f"Item with ID: {item_id} not found.")
            return
        
        # Check if the interactor is the owner of the product
        wallet = Wallet.get(Wallet.id == interaction.user.id)
        if product.owner != wallet:
            await interaction.response.send_message("You don't have the required permissions")
            return
        
        # Render product instance as dict
        product_dict = {
            "emoji": product.emoji,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "currency": product.currency.name,
            "is_active": product.is_active,
            "stock": product.stock
        }

        # Edit the product
        await create.create_product(interaction, product_info=product_dict)

async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(ShopGroupCommand(name="item", description="Manage your items"))