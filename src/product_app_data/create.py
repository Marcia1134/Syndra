import discord
from discord import ui
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from database.tables import Wallet, Product, Currency, Server

load_dotenv('config.env')

verbose = False
if getenv("DEBUG") == "True":
    verbose = True

# Embed Builder
class ProductEmbed(discord.Embed):
    def __init__(self, product : dict):
        super().__init__(title=product['name'], description=product['description'])
        self.add_field(name="Price", value=f"{product['price']} {product['currency']}", inline=False)
        self.add_field(name="Stock", value=product['stock'], inline=False)
        self.add_field(name="Is Active", value=product['is_active'], inline=False)

class Set_Product_Name_Modal(ui.Modal):
    def __init__(self, product : dict):
        super().__init__(timeout=None, title="Set Product Infomation")

        self.product_info = product

        self.product_name = ui.TextInput(label="Product Name", placeholder="Enter Product Name", required=True)
        self.product_description = ui.TextInput(label="Product Description", placeholder="Enter Product Description", required=True)
        
        self.add_item(self.product_name)
        self.add_item(self.product_description)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        
        self.product_info['name'] = self.product_name.value
        self.product_info['description'] = self.product_description.value
        
        await interaction.message.edit(embed=ProductEmbed(self.product_info))
        await interaction.response.send_message("Product Name and Description Set", ephemeral=True, delete_after=5)
        
        return

class Set_Product_Price_Modal(ui.Modal):
    def __init__(self, product : dict):
        super().__init__(timeout=None, title="Set Product Infomation")

        self.product_info = product

        self.product_price = ui.TextInput(label="Product Price", placeholder="Enter Product Price", required=True)
        self.product_currency = ui.TextInput(label="Product Currency", placeholder="Enter Product Currency", required=True)

        self.add_item(self.product_price)
        self.add_item(self.product_currency)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        
        # Check to see if price is a number
        if self.product_price.value.isnumeric():
            self.product_info['price'] = float(self.product_price.value)
        else:
            await interaction.response.send_message("Invalid Price, please try again!", ephemeral=True, delete_after=15)
            return
        
        # Check to see if currency exists
        try:
            Currency.get(Currency.name == self.product_currency.value)
        except:
            await interaction.response.send_message("Invalid Currency, please try again!", ephemeral=True, delete_after=15)
            return

        self.product_info['price'] = self.product_price.value
        self.product_info['currency'] = self.product_currency.value
        
        await interaction.message.edit(embed=ProductEmbed(self.product_info))
        await interaction.response.send_message("Product Price Set", ephemeral=True, delete_after=5)
        
        return

class Set_Product_Stock_Modal(ui.Modal):
    def __init__(self, product : dict):
        super().__init__(timeout=None, title="Set Product Infomation")

        self.product_info = product

        self.product_stock = ui.TextInput(label="Product Stock", placeholder="Enter Product Stock", required=True)
        
        self.add_item(self.product_stock)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        
        # Check to see if stock is a number
        if self.product_stock.value.isnumeric():
            self.product_info['stock'] = int(self.product_stock.value)
        else:
            await interaction.response.send_message("Invalid Stock, please try again!", ephemeral=True, delete_after=15)
            return
        
        self.product_info['stock'] = self.product_stock.value
        
        await interaction.message.edit(embed=ProductEmbed(self.product_info))
        await interaction.response.send_message("Product Stock Set", ephemeral=True, delete_after=5)
        
        return

class CreateProductView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.product_info = {
            "name" : "Place Holder Product Name",
            "description" : "Place Holder Product Description",
            "price" : 0,
            "currency" : "???",
            "is_active" : False,
            "stock" : 0
        }

    @ui.button(label="Product Name", emoji="📦", style=discord.ButtonStyle.green)
    async def set_product_name(self, interaction : discord.Interaction, button : ui.Button):
        await interaction.response.send_modal(Set_Product_Name_Modal(self.product_info))
        return
    
    @ui.button(label="Product Price", emoji="💰", style=discord.ButtonStyle.green)
    async def set_product_price(self, interaction : discord.Interaction, button : ui.Button):
        await interaction.response.send_modal(Set_Product_Price_Modal(self.product_info))
        return
    
    @ui.button(label="Set Product Active", emoji="🟢", style=discord.ButtonStyle.green)
    async def set_product_active(self, interaction : discord.Interaction, button : ui.Button):
        
        self.product_info['is_active'] = not self.product_info['is_active']
        
        # Adaptive Button
        if self.product_info['is_active']:
            button.label = "Set Product Inactive"
            button.emoji = "🔴"
            button.style = discord.ButtonStyle.red
        else:
            button.label = "Set Product Active"
            button.emoji = "🟢"
            button.style = discord.ButtonStyle.green
        
        await interaction.message.edit(embed=ProductEmbed(self.product_info) ,view=self)
        await interaction.response.send_message("Product Active Status Set", ephemeral=True, delete_after=5)
        
        return
    
    @ui.button(label="Product Stock", emoji="📦", style=discord.ButtonStyle.green)
    async def set_product_stock(self, interaction : discord.Interaction, button : ui.Button):
        await interaction.response.send_modal(Set_Product_Stock_Modal(self.product_info))
        return
    
    @ui.button(label="Create Product", emoji="📦", style=discord.ButtonStyle.blurple)
    async def create_product(self, interaction : discord.Interaction, button : ui.Button):
        
        # Check to see if product already exists
        try:
            Product.get(Product.name == self.product_info['name'])
        except:
            pass
        else:
            await interaction.response.send_message(f"Product named: {self.product_info['name']} already exists, try another name!", ephemeral=True, delete_after=5)
            return

        # Check if interaction user has a wallet
        try:
            Wallet.get(Wallet.user == interaction.user.id)
        except:
            # Create user wallet and continue
            Wallet.create(
                id=interaction.user.id,
                server=Server.get(Server.id == interaction.guild.id),
                currency=Currency.get(Currency.server == interaction.guild.id),
                balance=0
            )
            pass

        # Create Product
        Product.create(
            owner=Wallet.get(Wallet.id == interaction.user.id),
            name=self.product_info['name'],
            description=self.product_info['description'],
            price=self.product_info['price'],
            is_active=self.product_info['is_active'],
            stock=self.product_info['stock']
        )

        await interaction.response.send_message("Product Created!", ephemeral=True, delete_after=5)
        
        return

async def create_product(interaction : discord.Interaction) -> None:
    
    await interaction.response.send_message(
        
        embed=ProductEmbed({
            "name" : "Place Holder Product Name",
            "description" : "Place Holder Product Description",
            "price" : 0,
            "currency" : "???",
            "is_active" : False,
            "stock" : 0
            }),
     
    view=CreateProductView())

    return