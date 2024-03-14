import discord 
from discord import app_commands
from discord.ext import commands
from database.tables import Wallet, Product, Currency, Roles, Server

class ShopCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="shop", description="View the shop")
    async def shop(self, interaction : discord.Interaction) -> None:

        # Check if Role exsits for server
        try:
            role = Roles.get(Roles.server == interaction.guild.id)
        except:
            # Create role if it doesn't exist
            shop_role = interaction.guild.create_role(name="shop", color=discord.Color.blue())
            role = Roles.create(server=Server.get_by_id(interaction.guild.id), role=shop_role.id, type=0)
            # Check if syndra category exists
            try:
                category = discord.utils.get(interaction.guild.categories, name="Syndra")
            except:
                # Create category if it doesn't exist
                category = await interaction.guild.create_category("Syndra")
            # Overwrites permssions to only allow the bot to send messages
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            interaction.guild.create_text_channel(name="shop", category=category, overwrites=overwrites)
            pass

        shop_channels = []
        for channel in interaction.guild.channels:
            if channel.permissions_for(interaction.guild.get_role(role.role)).send_messages:
                shop_channels.append(channel)

        if len(shop_channels) == 0:
            interaction.response.send_message("No shop found")
        else:
            pass

        class ShopView(discord.ui.View):
            def __init__(self, shop_channels):
                super().__init__()

                options = []
                for channel in shop_channels:
                    options.append(discord.SelectOption(label=channel.name, value=channel.id))

                self.channel_selection = discord.ui.Select(placeholder="Select a shop", options=options, custom_id="shop_select", max_values=1, min_values=1)

                self.add_item(self.channel_selection)

            async def interaction_check(self, interaction: discord.Interaction):
                channel = interaction.guild.get_channel(int(interaction.data["values"][0]))
                await interaction.response.send_message(f"Selected {channel.name}")

                async def render_pipeline(channel_id = int(interaction.data["values"][0]), ):

                    def embed_builder(shop_config, ):
                        embed = discord.Embed(title=f"{shop_config.name}", description=f"{shop_config.description}")
                        return embed
                    


        await interaction.response.send_message("Select a shop", view=ShopView(shop_channels))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ShopCommand(bot))