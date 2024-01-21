import discord
from os import getenv
from dotenv import load_dotenv
from discord.ext import commands
import peewee as pw
import json

load_dotenv(".env")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

db = pw.SqliteDatabase("database.db")
db.connect()

class BaseModel(pw.Model):
    class Meta:
        database = db

class Server_configs(BaseModel):
    server_id = pw.IntegerField(primary_key=True)
    whitelist = pw.TextField() #JSON
    role_config = pw.TextField() #JSON

class Currencies(BaseModel):
    server_id = pw.IntegerField(primary_key=True)
    currency_name = pw.IntegerField()
    role_pay = pw.TextField() #JSON

class Profiles(BaseModel):
    server_id = pw.IntegerField()
    user_id = pw.IntegerField()
    amount = pw.IntegerField()

class Trades(BaseModel):
    trade_id = pw.AutoField(primary_key=True)
    user_id_sender = pw.IntegerField()
    user_id_receiver = pw.IntegerField()
    currency_name = pw.IntegerField()
    amount = pw.IntegerField()

db.create_tables([Currencies, Profiles, Trades, Server_configs])

@bot.event
async def on_ready():
    print("Bot is ready!")
    await tree.sync()  

@tree.command(name="setup")
async def setup(interaction: discord.Interaction):
    # scan for existing setup
    exists = True
    try:
        Server_configs.get_by_id(interaction.guild.id)
    except Exception as e:
        exists = False
    if exists:
        await interaction.response.send_message("This Channel has an existing setup, to have this set up removed, contact an admin.", ephemeral=True)
        return
    
    # send setup message
    await interaction.channel.send("Your server is being set up, please wait...")
    
    # 5.1 Currency Set Up
    class currency_setup_modal(discord.ui.Modal):
        def __init__(self):
            super().__init__(title="Currency Setup", timeout=None)
            # Text Inputs
            self.currency_name = discord.ui.TextInput(label="Currency Name", placeholder="Currency Name", min_length=1, max_length=20, required=True)
            self.add_item(self.currency_name)
        
        async def on_submit(self, interaction: discord.Interaction):
            
            # 5.2 getting whitelist
            class whitelist_setup_view(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=None)
                

                options = [discord.SelectOption(label="/bal", value="bal")
                           ,discord.SelectOption(label="/trade", value="trade")
                           ,discord.SelectOption(label="/adopt", value="adopt")]
                @discord.ui.select(placeholder="Select a commands to whitelist", min_values=1, max_values=len(options), options=options)
                async def whitelist(self, interaction: discord.Interaction, select: discord.ui.Select):
                    # Create Server Config
                    try:
                        Server_configs.create(server_id=interaction.guild.id, whitelist=json.dumps(select.values, indent=4), role_config=json.dumps({"none" : "none"}, indent=4))
                    except Exception as e:
                        await interaction.channel.send(f"Something Went Wrong! /nError: ```{e}```", ephemeral=True)
                        return
                    
                    return
            
            await interaction.response.send_message("Select the commands you want to whitelist", view=whitelist_setup_view(), ephemeral=True)

            # Create Currency
            try:
                Currencies.create(server_id=interaction.guild.id, currency_name=self.currency_name.value, role_pay=json.dumps({"none" : "none"}, indent=4))
            except Exception as e:
                await interaction.channel.send(f"Something Went Wrong! /nError: ```{e}```")
                return
            # Send Success Message
            await interaction.channel.send("Currency Created!")

            return

    await interaction.response.send_modal(currency_setup_modal())

    
@tree.command(name="adopt") # DEBUG
async def adopt(interaction: discord.Interaction):
    try:
        Profiles.create(server_id=interaction.guild.id, user_id=interaction.user.id, amount=Currencies.get_by_id(interaction.guild.id).currency_default)
        await interaction.response.send_message("Adopted!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(e, ephemeral=True)

@tree.command(name="bal")
async def bal(interaction: discord.Interaction, all: bool = False):
    try:
        if all:
            stuff = ''
            for profile in Profiles.select().where(Profiles.user_id == interaction.user.id):
                stuff += f"{profile.amount} {Currencies.get_by_id(profile.server_id).currency_name}\n"
            await interaction.response.send_message(stuff, ephemeral=True)
        else:
            await interaction.response.send_message(f"{Profiles.select().where(Profiles.user_id == interaction.user.id).where(Profiles.server_id == interaction.guild.id).get().amount} {Currencies.get_by_id(interaction.guild_id).currency_name}", ephemeral=True)
    except Exception as e:    
        Profiles.create(server_id=interaction.guild.id, user_id=interaction.user.id, amount=0)
        await interaction.response.send_message("You do not have a profile, A profile is being created, try this command again!", ephemeral=True)
    

class confirmation(discord.ui.View):
    """
    Confirmation View

    --ARGS--
    execuatable: function to execute
    **kargs: keyword arguments to pass to the function
    """
    def __init__(self, execuatable, **kargs):
        super().__init__()
        self.execuatable = execuatable
        self.kargs = kargs

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.execuatable(**self.kargs)
        await interaction.response.edit_message(view=None, content="Operation Successful!")

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=None, content="Operation Cancelled!")

@tree.command(name="trade")
async def trade(interaction: discord.Interaction, receiver: discord.User, currency_name: str, amount: int):
    # Check Logic
    if amount < 0:
        await interaction.response.send_message("You can't trade negative amounts!", ephemeral=True)
    elif amount == 0:
        await interaction.response.send_message("You can't trade 0!", ephemeral=True)
    else:
        # Grab Profile
        try:
            profile = Profiles.select().where(Profiles.user_id == interaction.user.id).where(Profiles.server_id == interaction.guild.id).get()
        except Exception as e:
            await interaction.response.send_message("You don't have a profile in this server!", ephemeral=True)
        # Check if user has enough money
        if amount > profile.amount:
            await interaction.response.send_message("You don't have enough money!", ephemeral=True)
        else:
            # Trade Logic
            async def trade_logic(interaction: discord.Interaction, receiver: discord.User, currency_name: str, amount: int):
                # Grab Sender Profile
                sender_profile = Profiles.select().where(Profiles.user_id == interaction.user.id).where(Profiles.server_id == interaction.guild.id).get()
                # Grab Receiver Profile
                try:
                    receiver_profile = Profiles.select().where(Profiles.user_id == receiver.id).where(Profiles.server_id == interaction.guild.id).get()
                except Exception as e:
                    Profiles.create(server_id=interaction.guild.id, user_id=receiver.id, amount=Currencies.get_by_id(interaction.guild.id).currency_default)
                    receiver_profile = Profiles.select().where(Profiles.user_id == receiver.id).where(Profiles.server_id == interaction.guild.id).get()
                    return
                # Update Sender Profile
                sender_profile.amount -= amount
                sender_profile.save()
                # Update Receiver Profile
                receiver_profile.amount += amount
                receiver_profile.save()
                # Create Trade
                Trades.create(user_id_sender=interaction.user.id, user_id_receiver=receiver.id, currency_name=currency_name, amount=amount)

            # Send Confirmation with trade logic
            await interaction.response.send_message(f"Are you sure you want to trade {amount} {currency_name} to {receiver.mention}?", view=confirmation(trade_logic, interaction=interaction, receiver=receiver, currency_name=currency_name, amount=amount), ephemeral=True)

@bot.event
async def on_member_join(member: discord.Member):
    try:
        Profiles.create(server_id=member.guild.id, user_id=member.id, amount=Currencies.get_by_id(member.guild.id).currency_default)
    except Exception as e:
        print(e)

@bot.event
async def on_member_remove(member: discord.Member):
    try:
        Profiles.get_by_id(member.id).delete_instance()
    except Exception as e:
        print(e)

@bot.command(name="deleteme")
async def deleteme(ctx: commands.Context):
    Profiles.select().where(Profiles.user_id == ctx.author.id).where(Profiles.server_id == ctx.guild.id).get().delete_instance()

@bot.command(name="add_amount")
async def add_amount(ctx: commands.Context, who : discord.User, amount: int):
    profile = Profiles.select().where(Profiles.user_id == who.id).where(Profiles.server_id == ctx.guild.id).get()
    profile.amount += amount
    profile.save()

bot.run(getenv("DISCORD_TOKEN"))