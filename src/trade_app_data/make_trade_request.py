import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from database.tables import Wallet, Product, Mail, Transaction, Currency, Server
from datetime import datetime

load_dotenv('config.env')

verbose = False
if getenv("DEBUG") == "True":
    verbose = True

'''
ERRORS:

0 - Sender doesn't have a wallet
1 - Reciever doesn't have a wallet
2 - Product doesn't exist
3 - Product can't be traded
4 - Sender doesn't have enough money
'''

async def main(bot : commands.bot, 
               interaction : discord.Interaction, 
               sender : discord.User, 
               reciever : discord.User, 
               product_id : int) -> None:
    
    # Debug
    if verbose:
        print("Iitializing trade request...")
        print("Checking if trade is possible...")

    # Check if Users have Wallets
    try:
        Wallet.get(Wallet.user == sender.id)
    except:
        if verbose:
            print("Sender doesn't have a wallet")
        await interaction.channel.send(f"{sender.mention} doesn't have a wallet.")
        return 0 # Sender doesn't have a wallet
    
    try:
        Wallet.get(Wallet.user == reciever.id)
    except:
        if verbose:
            print("Reciever doesn't have a wallet")
        await interaction.channel.send(f"{reciever.mention} doesn't have a wallet.")
        return 1 # Reciever doesn't have a wallet
    
    # Check if Product Exists
    try:
        Product.get(Product.id == product_id)
    except:
        if verbose:
            print("Product doesn't exist")
        await interaction.channel.send(f"Product {product_id} doesn't exist.")
        return 2 # Product doesn't exist
    
    # Check if product is active && is in stock
    product = Product.get(Product.id == product_id)
    if product.is_active == False:
        await interaction.channel.send(f"Product {product_id} is not actively being sold.")
        return 3 # Product can't be traded
    if product.stock > 0:
        pass
    else:
        await interaction.channel.send(f"Product {product_id} is out of stock.")
        return 3 # Product can't be traded

    # Check sender wallet
    sender_wallet = Wallet.get(Wallet.user == sender.id)
    if sender_wallet.balance < Product.get(Product.id == product_id).price:
        await interaction.channel.send(f"{sender.mention} doesn't have enough money to buy product {product_id}.")
        return 4 # Sender doesn't have enough money

    # Version 0.1.1.1 - trading

    command_version = "0.1.1.1"

    # Verify with Sender
    await interaction.channel.send(f"Are you sure you want to trade {product_id} with {reciever.mention}? (yes/no)")
    def check(m):
        return m.author == sender and m.content.lower() in ["yes", "no"]
    msg = await bot.wait_for('message', check=check)
    if msg.content.lower() == "no":
        return
    elif msg.content.lower() == "yes":
        pass

    # Notify Sender of beta version
    await interaction.channel.send(f"This is a beta version of the trade command. Please report any bugs to the developer. More updates to this command and more will be coming soon!\nVersion: {command_version}")

    # Create transaction instance

    # Get wallet of sender
    sender_wallet = Wallet.get(Wallet.user == sender.id)

    # Get wallet of reciever
    reciever_wallet = Wallet.get(Wallet.user == reciever.id)

    # Get currency

    # Get server
    server = Server.get(Server.id == interaction.guild.id)

    # Fetch currency
    currency = Currency.get(Currency.server == server.id)

    # Create transaction
    Transaction.create(sender=sender_wallet.id, 
                       reciever=reciever_wallet.id, 
                       currency=currency, 
                       product_id=product_id, 
                       date=datetime.now())

    # Create mail instance for reciever
    Mail.create(wallet=reciever_wallet.id, 
                transaction=Transaction.get(Transaction.sender == sender_wallet.id), 
                read=False)
    
    # Ping reciever
    await reciever.send(f"You have a new trade request from {sender.mention}.")

    return