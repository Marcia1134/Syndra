import discord 
from discord import app_commands
from discord.ext import commands
from database.tables import Wallet, Product, Currency, Server, ShopChannels

class ShopCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="shop", description="View the shop")
    async def shop(self, interaction : discord.Interaction) -> None:

        # Get the server
        server = Server.get_or_none(Server.id == interaction.guild.id)
        if server is None:
            await interaction.response.send_message("Shop has not been activated")
            return

        # Fetch all shop channels
        shop_channels = ShopChannels.select().where(ShopChannels.server == server).execute()
        if len(shop_channels) == 0:
            await interaction.response.send_message("Shop has not been activated")
            return
        
        class ShopChannelSelection(discord.ui.View):
            def __init__(self, channels):
                super().__init__(timeout=None)

                options = []
                for channel in channels:
                    options.append(discord.SelectOption(label=channel.channel.name, value=str(channel.channel.id)))

                self.select = discord.Select(
                    placeholder="Select a shop channel",
                    options=options
                )
                self.add_item(self.select)

            def interaction_check(self, interaction: discord.Interaction) -> bool:
                # Fetch Channel
                channel = interaction.guild.get_channel(int(self.select.values[0]))
                if channel is None:
                    return False
                channel.send("Shop has been activated")

    @app_commands.command(name="shop_activate", description="Activate the shop")
    async def shop_activate(self, interaction : discord.Interaction) -> None:

        # Add the shop channel to the database
        server = Server.get_or_none(Server.id == interaction.guild.id)
        if server is None:
            server = Server.create(id=interaction.guild.id)

        shop_channel = ShopChannels.get_or_none(ShopChannels.server == server)
        if shop_channel is None:
            ShopChannels.create(server=server, channel=interaction.channel.id)
        else:
            shop_channel.channel = interaction.channel.id
            shop_channel.save()

        # Update Channel Permssions
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        await interaction.channel.set_permissions(interaction.guild.me, send_messages=True)

        await interaction.response.send_message("Shop has been activated")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ShopCommand(bot))