import discord
from os import getenv
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
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
    channels = pw.TextField() #JSON

class Currencies(BaseModel):
    server_id = pw.IntegerField(primary_key=True)
    currency_name = pw.IntegerField()
    role_allowance = pw.TextField() #JSON

class Profiles(BaseModel):
    server_id = pw.IntegerField()
    user_id = pw.IntegerField()
    amount = pw.IntegerField()

class Trades(BaseModel):
    trade_id = pw.AutoField(primary_key=True)
    user_id_customer = pw.IntegerField()
    user_id_seller = pw.IntegerField()
    currency_name = pw.IntegerField()
    product_url = pw.TextField(default="none")
    amount = pw.IntegerField()

class Stasis(BaseModel):
    stasis_id = pw.AutoField(primary_key=True)
    user_id_customer = pw.IntegerField()
    user_id_seller = pw.IntegerField()
    currency_name = pw.IntegerField()
    amount = pw.IntegerField()
    type = pw.IntegerField() # 0 = trade,
    completed = pw.BooleanField()

class Mail_Tickets(BaseModel):
    ticket_id = pw.AutoField(primary_key=True)
    user_id = pw.IntegerField(unique=True)
    channel_id = pw.IntegerField()

class Verification_Gates(BaseModel):
    gate_id = pw.AutoField(primary_key=True)
    stage = pw.IntegerField()
    stasis = pw.ForeignKeyField(Stasis, backref="verification_gate")

db.create_tables([Currencies, Profiles, Trades, Server_configs, Stasis, Mail_Tickets, Verification_Gates])

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
        await interaction.response.send_message("This Channel has an existing setup, to have this set up removed, contact an admin.")
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
            
            # Set Up Channels
            
            class channel_setup_view(discord.ui.View):
                def __init__(self, currency_name):
                    super().__init__(timeout=None)
                    self.currency_name = currency_name
                
                @discord.ui.button(label="Create Channels", style=discord.ButtonStyle.green, custom_id="create_channels")
                async def create_channels(self, interaction: discord.Interaction, button: discord.ui.Button):
                    # Create Category
                    try:
                        category = await interaction.guild.create_category("Syndra", overwrites=None, reason="Syndra Setup")
                    except Exception as e:
                        await interaction.channel.send(f"Something Went Wrong! /nError: ```{e}```")
                        print("Error: ", e)
                        return
                    # Create Channels
                    try:
                        await interaction.guild.create_text_channel("Syndra-Chat", category=category, overwrites=None, reason="Syndra Setup")
                        await interaction.guild.create_text_channel("Syndra-Commands", category=category, overwrites=None, reason="Syndra Setup")
                        await interaction.guild.create_text_channel("Syndra-Trade", category=category, overwrites=None, reason="Syndra Setup")
                    except Exception as e:
                        await interaction.channel.send(f"Something Went Wrong! /nError: ```{e}```")
                        print("Error: ", e)
                        return
                    # Send Success Message
                    await interaction.channel.send("Channels Created!")
                    return

            await interaction.channel.send("Syndra needs a couple channels to work well!\n> --Syndra Catergory-- \n> Syndra-Chat \n> Syndra-Commands \n> Syndra-Trade\n\nThe Above commands must be included! If you want we can create that all for you! Or you can use a command to set everything up yourself!  \n\n```if you want to set things up yourself, use the /setup_channels_manual command!\nHowever if you want automatic setup, please click the button below.```\n\nIf you need assistance in manual setup, please use the /setup_channels_manual_help", view=channel_setup_view(self.currency_name.value))

            # 5.2 getting whitelist
            class whitelist_setup_view(discord.ui.View):
                def __init__(self, currency_name):
                    super().__init__(timeout=None)
                    self.currency_name = currency_name
                
                options = [discord.SelectOption(label="/bal", value="bal")
                           ,discord.SelectOption(label="/trade", value="trade")
                           ,discord.SelectOption(label="/adopt", value="adopt")]
                
                @discord.ui.select(placeholder="Select a commands to whitelist", min_values=1, max_values=len(options), options=options)
                async def whitelist(self, interaction: discord.Interaction, select: discord.ui.Select):
                    # Create Server Config
                    try:
                        Server_configs.create(server_id=interaction.guild.id, whitelist=json.dumps(select.values, indent=4), channels=json.dumps({"category" : "none", "chat" : "none", "commands" : "none", "trade" : "none"}, indent=4))
                    except Exception as e:
                        await interaction.channel.send(f"Something Went Wrong! /nError: ```{e}```")
                        print("Error: ", e)
                        return
                    # Create currency without role allowance config
                    try:
                        Currencies.create(server_id=interaction.guild.id, currency_name=self.currency_name, role_allowance=json.dumps({"none" : "none"}, indent=4))
                    except Exception as e:
                        await interaction.channel.send(f"Something Went Wrong! /nError: ```{e}```")

                    # Ask user to set up role allowance
                    await interaction.channel.send("you need to set up up your role allowance to complete the setup, please use the /role_allowance_help command to set it up.")
                    
                    return
            
            await interaction.response.send_message("Select the commands you want to whitelist", view=whitelist_setup_view(self.currency_name.value))
            
            # DEPRECATED 
            # Could not handle more then 25 roles in the dropdown menu, see [discord.SelectOption(label=role.name, value=str(role.id)) for role in roles] for more info
            '''# View Class for Role Pay
            class role_pay_view(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=None)
                    self.role_pay = {}

                    # Get all roles in the server
                    roles = interaction.guild.roles
                    print([discord.SelectOption(label=role.name, value=str(role.id)) for role in roles])
                    options = [discord.SelectOption(label=role.name, value=str(role.id)) for role in roles]

                    # Create the selection menu
                    self.role_select = discord.ui.Select(placeholder="Select a role", options=options)
                    self.add_item(self.role_select)

                @discord.ui.button(label="Add Role", style=discord.ButtonStyle.green, custom_id="add_role")
                async def add_role(self, interaction: discord.Interaction, button: discord.ui.Button):
                    # Get the selected role from the selection menu
                    selected_role = self.role_select.values[0]
                    
                    # Send a modal to ask for the amount
                    class amount_modal(discord.ui.Modal):
                        def __init__(self):
                            super().__init__(title="Role Pay Amount", timeout=None)
                            self.amount = discord.ui.TextInput(label="Amount", placeholder="Enter the amount", min_length=1, max_length=20, required=True)
                            self.add_item(self.amount)

                        async def on_submit(self, interaction: discord.Interaction):
                            # Get the amount from the modal response
                            amount = int(self.amount.value)
                            
                            # Add the role and amount to the role_pay dictionary
                            self.role_pay[selected_role] = amount
                            
                            # Send success message
                            await interaction.response.send_message("Role Added!")
                    
                    # Send the amount modal
                    await interaction.response.send_modal(amount_modal())
                
                @discord.ui.button(label="Done", style=discord.ButtonStyle.green, custom_id="done")
                async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
                    # Send Success Message
                    await interaction.response.edit_message(view=None, content="Role Pay Set Up!")
                    # Create Currency
                    try:
                        Currencies.create(server_id=interaction.guild.id, currency_name=self.currency_name.value, role_pay=json.dumps(self.role_pay, indent=4))
                    except Exception as e:
                        await interaction.channel.send(f"Something Went Wrong! /nError: ```{e}```")
                        return
                    # Send Success Message
                    await interaction.channel.send("Currency Created!")
                    return
                
                @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, custom_id="cancel")
                async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
                    # Send Success Message
                    await interaction.response.edit_message(view=None, content="Role Pay Cancelled!")
                    return
                
            await interaction.channel.send("Set up your role pay", view=role_pay_view())'''
                
            return
    
    await interaction.response.send_modal(currency_setup_modal())

@tree.command(name="setup_channels_manual_help")
async def setup_channels_manual_help(interaction: discord.Interaction):
    await interaction.response.send_message("When using the /setup_channels_manual command you will see four boxes. Please select the channel that you want to set as each in the following order. 1. Catergory, 2. Syndra-chat channel, 3. syndra-commands, 4. syndra-trade. If you mess up the order you will need to redo the command.")

@tree.command(name="setup_channels_manual")
async def setup_channels_manual(interaction: discord.Interaction, category: discord.CategoryChannel, chat: discord.TextChannel, commands: discord.TextChannel, trade: discord.TextChannel):
    # Write channel ids to db
    Server_config_instance = Server_configs.get_by_id(interaction.guild.id)
    Server_config_instance.channels = json.dumps({"category" : str(category.id), "chat" : str(chat.id), "commands" : str(commands.id), "trade" : str(trade.id)}, indent=4)
    Server_config_instance.save()
    # Send Success Message
    await interaction.channel.send("Channels Stored!")

@tree.command(name="role_allowance_help")
async def role_allowance_help(interaction: discord.Interaction):
    await interaction.response.send_message("# SETTING UP A ROLE\nYou need to use the /role_allowance command! This command will ask for two things. the `role` you want to asssign payment to, and the `amount` you want to pay in. Please note the following:\nIn order to set a `role`, you must **MENTION** the role (@staff), once it turns BLUE in appearence, you can click to amount.\nIn order to set an `amount`, you must input aa number that does NOT contain ANY other characters. Please ***__only__*** use characters 0-9, anything else WILL BE REJECTED.")

@tree.command(name="role_allowance")
async def role_allowance(interaction: discord.Interaction, role: discord.Role, amount: int):
    # Check if setup exists
    try:
        Server_configs.get_by_id(interaction.guild.id)
    except Exception as e:
        await interaction.response.send_message("This Channel does not have an existing setup, to set up, use the /setup command.")
        return
    
    # Check if currency exists
    try:
        Currencies.get_by_id(interaction.guild.id)
    except Exception as e:
        await interaction.response.send_message("This Channel does not have an existing currency, to set up, use the /setup command.")
        return
    
    # Grab Role Allowance config JSON
    role_allowance = json.loads(Currencies.get_by_id(interaction.guild.id).role_allowance)
    
    # Check if role is already in the config
    if str(role.id) in role_allowance:
        await interaction.response.send_message("This role is already in the config, to change the amount, use the /role_allowance_change command.")
        return
    
    # Add role to config
    role_allowance[str(role.id)] = amount

    # Update config
    Currency_instance = Currencies.get_by_id(interaction.guild.id)
    Currency_instance.role_allowance = json.dumps(role_allowance, indent=4)
    Currency_instance.save()

    # Send Success Message
    await interaction.response.send_message("Role Added!")

@tree.command(name="role_allowance_change")
async def role_allowance_change(interaction: discord.Interaction, role: discord.Role, amount: int):
    # Check if setup exists
    try:
        Server_configs.get_by_id(interaction.guild.id)
    except Exception as e:
        await interaction.response.send_message("This Channel does not have an existing setup, to set up, use the /setup command.")
        return
    
    # Check if currency exists
    try:
        Currencies.get_by_id(interaction.guild.id)
    except Exception as e:
        await interaction.response.send_message("This Channel does not have an existing currency, to set up, use the /setup command.")
        return
    
    # Grab Role Allowance config JSON
    role_allowance = json.loads(Currencies.get_by_id(interaction.guild.id).role_allowance)
    
    # Check if role is already in the config
    if str(role.id) not in role_allowance:
        await interaction.response.send_message("This role is not in the config, to add the role, use the /role_allowance command.")
        return
    
    # Change amount
    role_allowance[str(role.id)] = amount

    # Update config
    Currency_instance = Currencies.get_by_id(interaction.guild.id)
    Currency_instance.role_allowance = json.dumps(role_allowance, indent=4)
    Currency_instance.save()

    # Send Success Message
    await interaction.response.send_message("Role Amount Changed!")

@tree.command(name="role_allowance_remove")
async def role_allowance_remove(interaction: discord.Interaction, role: discord.Role):
    # Check if setup exists
    try:
        Server_configs.get_by_id(interaction.guild.id)
    except Exception as e:
        await interaction.response.send_message("This Channel does not have an existing setup, to set up, use the /setup command.")
        return
    
    # Check if currency exists
    try:
        Currencies.get_by_id(interaction.guild.id)
    except Exception as e:
        await interaction.response.send_message("This Channel does not have an existing currency, to set up, use the /setup command.")
        return
    
    # Grab Role Allowance config JSON
    role_allowance = json.loads(Currencies.get_by_id(interaction.guild.id).role_allowance)
    
    # Check if role is already in the config
    if str(role.id) not in role_allowance:
        await interaction.response.send_message("This role is not in the config, to add the role, use the /role_allowance command.")
        return
    
    # Remove role
    role_allowance.pop(str(role.id))

    # Update config
    Currency_instance = Currencies.get_by_id(interaction.guild.id)
    Currency_instance.role_allowance = json.dumps(role_allowance, indent=4)
    Currency_instance.save()

    # Send Success Message
    await interaction.response.send_message("Role Removed!")

@tree.command(name="role_allowance_list")
async def role_allowance_list(interaction: discord.Interaction):
    # Check if setup exists
    try:
        Server_configs.get_by_id(interaction.guild.id)
    except Exception as e:
        await interaction.response.send_message("This Channel does not have an existing setup, to set up, use the /setup command.")
        return
    
    # Check if currency exists
    try:
        Currencies.get_by_id(interaction.guild.id)
    except Exception as e:
        await interaction.response.send_message("This Channel does not have an existing currency, to set up, use the /setup command.")
        return
    
    # Grab Role Allowance config JSON
    role_allowance = json.loads(Currencies.get_by_id(interaction.guild.id).role_allowance)
    
    # Check if role is already in the config
    if len(role_allowance) == 0:
        await interaction.response.send_message("There are no roles in the config, to add a role, use the /role_allowance command.")
        return
    
    # Send Success Message
    await interaction.response.send_message(f"```json\n{json.dumps(role_allowance, indent=4)}\n```")

@tree.command(name="role_allowance_done")
async def role_allowance_done(interaction: discord.Interaction):
    # Check if setup exists
    try:
        Server_configs.get_by_id(interaction.guild.id)
    except Exception as e:
        await interaction.response.send_message("This Channel does not have an existing setup, to set up, use the /setup command.")
        return
    
    # Check if currency exists
    try:
        Currencies.get_by_id(interaction.guild.id)
    except Exception as e:
        await interaction.response.send_message("This Channel does not have an existing currency, to set up, use the /setup command.")
        return
    
    # Grab Role Allowance config JSON
    role_allowance = json.loads(Currencies.get_by_id(interaction.guild.id).role_allowance)

    # Check if role is already in the config
    if len(role_allowance) == 0:
        await interaction.response.send_message("There are no roles in the config, to add a role, use the /role_allowance command.")
        return
    
    async def role_allowance_completion_logic(interaction: discord.Interaction, role_allowance: dict):
        # Grab Currency
        currency = Currencies.get_by_id(interaction.guild.id)
        # Update Currency
        currency.role_allowance = json.dumps(role_allowance, indent=4)
        # Send Success Message
        await interaction.channel.send("You know, thank you.  Thank you... What else do I have to say? I mean honestly.You used all my commands and everything! Look at you! Using commands like that! Like a Wizzard ~~harry~~. Like a Wizard! You can do all that can't you. aint that just something.them fingers flying across the keyboard. Truely amazing.")
    
    await interaction.response.send_message("Are you sure you want to complete the role allowance setup?", view=confirmation(role_allowance_completion_logic, interaction=interaction, role_allowance=role_allowance))

@tree.command(name="adopt") # DEBUG
async def adopt(interaction: discord.Interaction):
    try:
        Profiles.create(server_id=interaction.guild.id, user_id=interaction.user.id, amount=Currencies.get_by_id(interaction.guild.id).currency_default)
        await interaction.response.send_message("Adopted!")
    except Exception as e:
        await interaction.response.send_message(e)

@tree.command(name="wallet") # Bal command changed to wallet
async def wallet(interaction: discord.Interaction, all: bool = False):
    try:
        if all:
            stuff = ''
            for profile in Profiles.select().where(Profiles.user_id == interaction.user.id):
                stuff += f"{profile.amount} {Currencies.get_by_id(profile.server_id).currency_name}\n"
            await interaction.response.send_message(stuff)
        else:
            await interaction.response.send_message(f"{Profiles.select().where(Profiles.user_id == interaction.user.id).where(Profiles.server_id == interaction.guild.id).get().amount} {Currencies.get_by_id(interaction.guild_id).currency_name}")
    except Exception as e:    
        Profiles.create(server_id=interaction.guild.id, user_id=interaction.user.id, amount=0)
        if all:
            stuff = ''
            for profile in Profiles.select().where(Profiles.user_id == interaction.user.id):
                stuff += f"{profile.amount} {Currencies.get_by_id(profile.server_id).currency_name}\n"
            await interaction.response.send_message(stuff)
        else:
            await interaction.response.send_message(f"{Profiles.select().where(Profiles.user_id == interaction.user.id).where(Profiles.server_id == interaction.guild.id).get().amount} {Currencies.get_by_id(interaction.guild_id).currency_name}")
        
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

# Get list of currencies
def get_currencies():
    # Grab Currencies
    currencies = Currencies.select().get()
    # Check if there are any currencies
    if len(currencies) == 0:
        return None
    
    list_of_choices = []

    for currency in currencies:
        list_of_choices.append(discord.SelectOption(label=currency.currency_name, value=currency.currency_name))
    
    return list_of_choices

# Stage 1 trade; initiating trade
@tree.command(name="trade")
@app_commands.choices(currency=[get_currencies()])
async def trade(interaction: discord.Interaction, seller: discord.User, currency_name: str, amount: int):
    # Check Logic
    if amount < 0:
        await interaction.response.send_message("You can't trade negative amounts!")
        return
    elif amount == 0:
        await interaction.response.send_message("You can't trade 0!")
        return
    # Grab Customer Profile
    try:
        profile = Profiles.select().where(Profiles.user_id == interaction.user.id).where(Profiles.server_id == interaction.guild.id).get()
    except Exception as e:
        await interaction.response.send_message("You don't have a profile in this server!")
    # Check if user has enough money
    if amount > profile.amount:
        await interaction.response.send_message("You don't have enough money!")
        return

    # Grab Stasis Gate State
    gate = Verification_Gates.select().where(Verification_Gates.stasis == Stasis.select().where(Stasis.user_id_customer == interaction.user.id).where(Stasis.user_id_receiver == seller.id).where(Stasis.currency_name == currency_name).where(Stasis.amount == amount).where(Stasis.type == 0).where(Stasis.completed == False).get()).get() # I HATE PEEWEE

    # Update Gate State
    gate.stage = 1 # Set State 1
    gate.save()

    # Trade Logic
    async def trade_logic(interaction: discord.Interaction, seller: discord.User, currency_name: str, amount: int):

        # Stage 2; ping seller

        # Grab server config
        server_config = Server_configs.get_by_id(interaction.guild.id)

        # Grab seller profile
        seller_profile = Profiles.select().where(Profiles.user_id == seller.id).where(Profiles.server_id == interaction.guild.id).get()

        # Grab trade notification channel
        trade_channel = discord.utils.get(interaction.guild.channels, id=int(json.loads(Server_configs.get_by_id(interaction.guild.id).channels)["trade"]))

        # Notify Seller
        await trade_channel.send(f"{interaction.user.mention} wants to trade {amount} {currency_name} from you", delete_after=1)

        # Create Stasis
        Stasis.create(user_id_customer=interaction.user.id, user_id_receiver=seller.id, currency_name=currency_name, amount=amount, type=0, completed=False)

        # DEPRECATED
        '''# Grab Sender Profile
        sender_profile = Profiles.select().where(Profiles.user_id == interaction.user.id).where(Profiles.server_id == interaction.guild.id).get()
        # Grab Receiver Profile
        try:
            receiver_profile = Profiles.select().where(Profiles.user_id == receiver.id).where(Profiles.server_id == interaction.guild.id).get()
        except Exception as e:
            Profiles.create(server_id=interaction.guild.id, user_id=receiver.id, amount=Currencies.get_by_id(interaction.guild.id).currency_default)
            receiver_profile = Profiles.select().where(Profiles.user_id == receiver.id).where(Profiles.server_id == interaction.guild.id).get()
            return

        # Create Stasis                 
        Stasis.create(user_id_customer=interaction.user.id, user_id_receiver=receiver.id, currency_name=currency_name, amount=amount, type=0, completed=False)

        # Create Gate
        gate_id = Verification_Gates.create(stage=0, stasis=Stasis.select().where(Stasis.user_id_customer == interaction.user.id).where(Stasis.user_id_receiver == receiver.id).where(Stasis.currency_name == currency_name).where(Stasis.amount == amount).where(Stasis.type == 0).where(Stasis.completed == False).get())

        # Remove Funds from Sender
        sender_profile.amount -= amount
        sender_profile.save()

        # Grab Trade notification channel
        trade_channel = discord.utils.get(interaction.guild.channels, id=int(json.loads(Server_configs.get_by_id(interaction.guild.id).channels)["trade"]))

        # Notify Receiver
        await trade_channel.send(f"{interaction.user.mention} wants to trade {amount} {currency_name} to you", delete_after=1)'''

        # DEPRECATED
        '''# Trade Logic for Receiver
        async def trade_logic_receiver(interaction: discord.Interaction, receiver: discord.User, currency_name: str, amount: int):
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
            Trades.create(user_id_customer=interaction.user.id, user_id_receiver=receiver.id, currency_name=currency_name, amount=amount)
            return
        
        # Send Confirmation with trade logic
        await interaction.channel.send(f"Are you sure you want to trade {amount} {currency_name} to {receiver.mention}?", view=confirmation(trade_logic_receiver, interaction=interaction, receiver=receiver, currency_name=currency_name, amount=amount))

        # DEPRECATED
        # Update Sender Profile
        sender_profile.amount -= amount
        sender_profile.save()
        # Update Receiver Profile
        receiver_profile.amount += amount
        receiver_profile.save()
        # Create Trade
        Trades.create(user_id_customer=interaction.user.id, user_id_receiver=receiver.id, currency_name=currency_name, amount=amount)'''

    # Send Confirmation with trade logic
    await interaction.response.send_message(f"Are you sure you want to trade {amount} {currency_name} to {seller.mention}?", view=confirmation(trade_logic, interaction=interaction, seller = seller, currency_name=currency_name, amount=amount))

@tree.command(name="mail")
async def mail(interaction: discord.Interaction):
    # Grab Stasis
    stasis = Stasis.select().where(Stasis.user_id_receiver == interaction.user.id).where(Stasis.completed == False)
    # Check if there are any stasis
    if len(stasis) == 0:
        await interaction.response.send_message("You have no mail!")
        return

    # Check if user has a mail ticket (if not create one)
    try:
        Mail_Tickets.select().where(Mail_Tickets.user_id == interaction.user.id).get()
    except Exception as e:
        # Create mail channel
        mail_channel = await interaction.guild.create_text_channel(f"mail-{interaction.user.name}", category = discord.utils.get(interaction.guild.categories, id=json.loads(Server_configs.select().where(Server_configs.server_id == interaction.guild.id).get().channels)["category"]), reason="Mail Ticket") # Please do not ask me what this line of code means. it is inline hell over here.
        # Create Mail Ticket
        Mail_Tickets.create(user_id=interaction.user.id, channel_id=mail_channel.id)
    
    # Grab Mail Ticket
    mail_ticket = Mail_Tickets.select().where(Mail_Tickets.user_id == interaction.user.id).get()
    print(mail_ticket.channel_id)
    mail_ticket_channel = discord.utils.get(interaction.guild.channels, id=mail_ticket.channel_id)

    # Check if mail ticket channel exists
    if mail_ticket_channel == None:
        await interaction.response.send_message("Your mail ticket channel does not exist! Something has gone wrong, please contact and Admin for further assistance. (Awaiting error code update)")
        return
    
    # Seller View Class (Stage 2)
    class seller_view(discord.ui.View):
        def __init__(self, interaction: discord.Interaction, stasis: Stasis):
            super().__init__(timeout=None)
            self.interaction = interaction
            self.stasis = stasis
        
        @discord.ui.button(label="Product Ready!", style=discord.ButtonStyle.green, custom_id="accept")
        async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Stage 3; ping customer

            # Step 3.1 Get img URL from seller (modal)
            class img_url_modal(discord.ui.modal):
                def __init__(self):
                    super().__init__(title="Image URL", timeout=None)
                    self.img_url = discord.ui.TextInput(label="Image URL", placeholder="Image URL", min_length=1, max_length=2000, required=True)
                    self.add_item(self.img_url)
                
                async def on_submit(self, interaction: discord.Interaction):

                    # Step 3.2 Filter image URL
                    
                    # [3.2.1] Check img URL filetype
                    if not self.img_url.value.endswith(".png") or not self.img_url.value.endswith(".jpg") or not self.img_url.value.endswith(".jpeg"):
                        await interaction.response.send_message("The image URL you provided is not a valid image URL!")
                        return
                    
                    # [3.2.2] Attempt to display IMG
                    async def image_confirmation_logic():

                        # Get Stasis
                        stasis = Stasis.select().where(Stasis.user_id_customer == self.stasis.user_id_customer).where(Stasis.user_id_receiver == self.stasis.user_id_receiver).where(Stasis.currency_name == self.stasis.currency_name).where(Stasis.amount == self.stasis.amount).where(Stasis.type == 0).where(Stasis.completed == False).get()

                        # Update Stasis
                        stasis.completed = True
                        stasis.save()

                        # Get Trade
                        trade = Trades.select().where(Trades.user_id_customer == self.stasis.user_id_customer).where(Trades.user_id_receiver == self.stasis.user_id_receiver).where(Trades.currency_name == self.stasis.currency_name).where(Trades.amount == self.stasis.amount).get()

                        # Update Trade
                        trade.product_url = self.img_url.value
                        trade.save()

                        # Grab trade notification channel
                        trade_channel = discord.utils.get(interaction.guild.channels, id=int(json.loads(Server_configs.get_by_id(interaction.guild.id).channels)["trade"]))

                        # Notify Customer
                        await trade_channel.send(f"{interaction.user.mention} wants to trade {self.stasis.amount} {self.stasis.currency_name} to you", delete_after=1)

                        # Send Success Message
                        await interaction.channel.send("Trade Stage 2 Completed!")
                        return
                    
                    try:
                        await interaction.response.send_message("Is this the image you want to send?", view=confirmation(image_confirmation_logic))
                    except Exception as e:
                        await interaction.channel.send(f"Something is wrong with the Image link provided. Please use the help button or for further assistance, contact an admin.")
                        print("Error: ", e)
                        return
            
            # Send Modal
            await interaction.response.send_modal(img_url_modal())

        @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, custom_id="cancel")
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):

            # Grab trade notification channel
            trade_channel = discord.utils.get(interaction.guild.channels, id=int(json.loads(Server_configs.get_by_id(interaction.guild.id).channels)["trade"]))

            # Notify Customer
            await trade_channel.send(f"{interaction.user.mention} wants to trade {self.stasis.amount} {self.stasis.currency_name} to you", delete_after=1)

            # Grab Stasis
            stasis = Stasis.select().where(Stasis.user_id_customer == self.stasis.user_id_customer).where(Stasis.user_id_receiver == self.stasis.user_id_receiver).where(Stasis.currency_name == self.stasis.currency_name).where(Stasis.amount == self.stasis.amount).where(Stasis.type == 0).where(Stasis.completed == False).get()

            # Update Stasis
            stasis.completed = True
            stasis.save()

            # Send Success Message
            await interaction.channel.send("Trade Cancelled!")

            return
        
        @discord.ui.button(label="Help", style=discord.ButtonStyle.grey, custom_id="help")
        async def help(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Hey there! Here is a quick explaination on how to get your Image URL! \n\n> We would reccomend the use of the free image host postimage. DUE NOTICE however, free hosting sites like this often contain vunarabilities and are often able to be viewed by anyone given the link (or if they simply guess the link.) It is highly encouraged you do not share sensitive media (such that contain any identifiable infomation, and explict media and etc.) If you wish to use another platform you are welcome, however here we will cover the guide for this website only!\n\n1. Head to https://postimages.org/ \n2. Click `Choose Images` and upload the image from your local disk. \n3. Wait for the upload to complete \n4. Copy the `Direct Link` and paste it into the modal. \n5. Click `Submit` and you are done! \n\n> If you need further assistance, please contact an admin.")

    # Customer View Class (Stage 3)
    class customer_view(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            

    # Send the view class
    for status in stasis:
        if interaction.user.id == status.user_id_seller:
            await mail_ticket_channel.send(f"{status.user_id_customer} wants to trade {status.amount} {status.currency_name} to you", view=seller_view(interaction=interaction, stasis=status))
            return
        elif interaction.user.id == status.user_id_customer:
            await mail_ticket_channel.send(f"{status.user_id_seller} wants to trade {status.amount} {status.currency_name} to you")
            return
        else:
            await interaction.response.send_message("Something went wrong! Please contact an admin for further assistance.")
            return

    '''# Send Mail to Sender
    async def trade_logic(interaction: discord.Interaction):
        # Grab Stasis
        stasis = Stasis.select().where(Stasis.user_id_receiver == interaction.user.id).where(Stasis.completed == False).get()
        
        # Grab Server Config
        server_config = Server_configs.get_by_id(interaction.guild.id)

        # Grab Gate
        gate = Verification_Gates.select().where(Verification_Gates.stasis == stasis).get()

        # Update Gate State
        gate.stage += 1
        gate.save()

        # Grab Mail Ticket
        mail_ticket = Mail_Tickets.select().where(Mail_Tickets.user_id == interaction.user.id).get().channel_id
        mail_ticket_channel = discord.utils.get(interaction.guild.channels, id=mail_ticket)

        # Check if mail ticket channel exists
        if mail_ticket_channel == None:
            await interaction.response.send_message("Your mail ticket channel does not exist!")
            return
        
        # Check if gate is complete
        if gate.stage == 1:
            # Grab Sender Profile
            sender_profile = Profiles.select().where(Profiles.user_id == stasis.user_id_customer).where(Profiles.server_id == interaction.guild.id).get()
            # Grab Receiver Profile
            receiver_profile = Profiles.select().where(Profiles.user_id == interaction.user.id).where(Profiles.server_id == interaction.guild.id).get()
            # Update Receiver Profile
            receiver_profile.amount += stasis.amount
            receiver_profile.save()
            # Create Trade
            Trades.create(user_id_customer=stasis.user_id_customer, user_id_receiver=interaction.user.id, currency_name=stasis.currency_name, amount=stasis.amount)
            # Update Stasis
            stasis.completed = True
            stasis.save()
            # Send Success Message
            await mail_ticket_channel.send("Trade Completed!")
            return
        elif gate.stage == 2:
            # Grab Sender Profile
            sender_profile = Profiles.select().where(Profiles.user_id == stasis.user_id_customer).where(Profiles.server_id == interaction.guild.id).get()
            # Grab Receiver Profile
            receiver_profile = Profiles.select().where(Profiles.user_id == interaction.user.id).where(Profiles.server_id == interaction.guild.id).get()
            # Update Sender Profile
            sender_profile.amount += stasis.amount
            sender_profile.save()
            # Update Stasis
            stasis.completed = True
            stasis.save()
            # Send Success Message
            await mail_ticket_channel.send("Trade Cancelled!")
            return
        else:
            await mail_ticket_channel.send("Something went wrong!")
            return'''

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

@bot.command(name="rm_currency")
async def rm_currency(ctx: commands.Context):
    try:
        Currencies.get_by_id(ctx.guild.id).delete_instance()
    except Exception as e:
        print(e)
    try:
        Server_configs.get_by_id(ctx.guild.id).delete_instance()
    except Exception as e:
        print(e)

bot.run(getenv("DISCORD_TOKEN"))