import discord
from discord import app_commands
from discord.ext import commands
from database.tables import Product, Wallet

class ProfileCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="profile", description="View the profile")
    async def profile(self, interaction : discord.Interaction, person : discord.User) -> None:
        products = Product.select().where(Product.owner == Wallet.select().where(Wallet.id == person.id)).execute()
        print(products)
        
        if len(products) == 0:
            await interaction.response.send_message("No products found.")
            return
        
        def render_split(product_list, embed):

            class ShopView(discord.ui.View):
                
                def render_buy_page(product):
                
                    class BuyView(discord.ui.View):
                        def __init__(self, product):
                            super().__init__(timeout=None)

                        @discord.ui.button(label="Yes", style=discord.ButtonStyle.primary, emoji="✅")
                        async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
                            pass

                        @discord.ui.button(label="No", style=discord.ButtonStyle.primary, emoji="❌")
                        async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
                            pass

                    embed = discord.Embed(title=f"{product.name}", description=f"Are you sure you want to buy {product.name} for {product.price}?")
                    return embed, BuyView(product)
                
                def __init__(self, product_list):
                    super().__init__()
                    
                    for product in product_list:
                        self.add_item(discord.ui.Button(style=discord.ButtonStyle.primary, emoji=product.emoji, custom_id=f"product_{product.id}"))
                    
                @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary, emoji="⬅️")
                async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
                    pass

                @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, emoji="➡️")
                async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
                    pass

                async def interaction_check(self, interaction: discord.Interaction):
                    print(interaction)
                    
                    ...

                    return

            for product in product_list:
                embed.add_field(name=f"{product.emoji} {product.name}", value=product.description, inline=False)
            return embed, ShopView(product_list)
        
        embed = discord.Embed(title=f"{person.name}'s Shop", description=f"Here are the products in {person.name}'s shop")
        pane = render_split(products, embed)
        await interaction.response.send_message(embed=pane[0], view=pane[1])

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ProfileCommand(bot))