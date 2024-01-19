import discord
from os import getenv
from dotenv import load_dotenv
from discord.ext import commands
import peewee as pw

load_dotenv(".env")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

db = pw.SqliteDatabase("database.db")
db.connect()

class Wallet(pw.Model):
    discord_id = pw.CharField(primary_key=True)
    curr = pw.CharField()
    amount = pw.IntegerField()

    class Meta:
        database = db

class Trades(pw.Model):
    trade_id = pw.AutoField(primary_key=True)
    discord_id_sender = pw.CharField()
    discord_id_receiver = pw.CharField()
    curr = pw.CharField()
    amount = pw.IntegerField()

    class Meta:
        database = db

db.create_tables([Wallet, Trades])

@bot.event
async def on_ready():
    print("Bot is ready!")
    await tree.sync()

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(name="balance")
async def balance(ctx):
    try:
        user = Wallet.get(discord_id=str(ctx.author.id))
    except:
        user = Wallet.create(discord_id=str(ctx.author.id), curr="USD", amount=0)
    await ctx.send(f"Your balance is {user.amount} {user.curr}")

class confirmation(discord.ui.View):
    def __init__(self, ctx, user, curr, amount):
        super().__init__()
        self.ctx = ctx
        self.user = user
        self.curr = curr
        self.amount = amount
        self.value = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        await interaction.response.edit_message(view=None)
        sender = Wallet.get(discord_id=str(self.ctx.user.id))
        receiver = Wallet.get(discord_id=str(self.user.id))
        sender.amount -= self.amount
        receiver.amount += self.amount
        sender.save()
        receiver.save()
        Trades.create(discord_id_sender=str(self.ctx.user.id), discord_id_receiver=str(self.user.id), curr=self.curr, amount=self.amount)
        await interaction.channel.send(f"Traded {self.amount} {self.curr} to {self.user.name}")

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        await interaction.response.edit_message(view=None)
        await interaction.channel.send("Cancelled")

@tree.command(name="trade")
async def trade(interaction : discord.Interaction, user: discord.User, curr: str, amount: int):
    if user == interaction.user:
        await interaction.response.send_message("You can't trade with yourself!")
        return
    sender = Wallet.get(discord_id=str(interaction.user.id))
    if sender.amount < amount:
        await interaction.response.send_message("You don't have enough money!")
        return
    if sender.curr != curr:
        await interaction.response.send_message("You don't have that currency!")
        return
    
    view = confirmation(interaction, user, curr, amount)
    await interaction.response.send_message(f"Are you sure you want to trade {amount} {curr} to {user.name}?", view=view)

@bot.command(name="add_amount")
async def add_amount(ctx, user_: discord.User, amount: int, curr: str):
    user = Wallet.get(discord_id=str(user_.id))
    user.amount += amount
    user.curr = curr
    user.save()
    await ctx.send(f"Added {amount} to {user_.name}'s balance")

bot.run(getenv("DISCORD_TOKEN"))