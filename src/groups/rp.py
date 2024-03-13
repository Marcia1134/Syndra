from discord import app_commands, Interaction
from discord.ext import commands
from database import tables
from dotenv import load_dotenv
from os import getenv

load_dotenv('config.env')

verbose = False
if getenv("DEBUG") == "True":
    verbose = True

class RPGroup(app_commands.Group):

    @app_commands.command(name="add", description="Add a new role pay entry")
    async def add(self, interaction : Interaction, role : str, amount : int) -> None:
        # Check for admin permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have the required permissions")
            return

        # Create a new role pay entry in the database
        tables.RolePay.create(server=tables.Server.get_by_id(interaction.guild_id), role=role, amount=amount)
        if verbose:
            print(f"Role {role} has been added to server {interaction.guild_id}")

        # Send a response message with the entered role pay details
        await interaction.response.send_message(f"Role: {role}\nAmount: {amount}")

    @app_commands.command(name="remove", description="Remove a role pay entry")
    async def remove(self, interaction : Interaction, role : str) -> None:
        # Check for admin permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have the required permissions")
            return

        # Check if the role pay entry exists
        rolepay = tables.RolePay.get_or_none(server=interaction.guild_id, role=role)
        if rolepay is None:
            await interaction.response.send_message(f"Role: {role} not found")
            return

        # Delete the role pay entry from the database
        tables.RolePay.delete().where(tables.RolePay.server == interaction.guild_id, tables.RolePay.role == role).execute()
        if verbose:
            print(f"Role {role} has been removed from server {interaction.guild_id}")

        # Send a response message with the removed role pay details
        await interaction.response.send_message(f"Role: {role} has been removed")

    @app_commands.command(name="list", description="List all role pay entries")
    async def list(self, interaction : Interaction) -> None:
        # Check for admin permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have the required permissions")
            return

        # Retrieve all role pay entries from the database
        rolepay = tables.RolePay.select().where(tables.RolePay.server == interaction.guild_id)
        rolepay_list = ""
        for role in rolepay:
            rolepay_list += f"Role: {role.role} Amount: {role.amount}\n"
        if rolepay_list == "":
            rolepay_list = "No role pay entries found"
        if verbose:
            print(f"Listing all role pay entries for server {interaction.guild_id}")

        # Send a response message with the role pay details
        await interaction.response.send_message(rolepay_list)

    @app_commands.command(name="edit", description="Edit a role pay entry")
    async def edit(self, interaction : Interaction, role : str, amount : int) -> None:
        # Check for admin permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have the required permissions")
            return

        # Check if the role pay entry exists
        rolepay = tables.RolePay.get_or_none(server=interaction.guild_id, role=role)
        if rolepay is None:
            # Create entry if it doesn't exist
            tables.RolePay.create(server=tables.Server.get_by_id(interaction.guild_id), role=role, amount=amount)
            if verbose:
                print(f"Role {role} has been added to server {interaction.guild_id}")
            return

        # Update the role pay entry in the database
        tables.RolePay.update(amount=amount).where(tables.RolePay.server == interaction.guild_id, tables.RolePay.role == role).execute()
        if verbose:
            print(f"Role {role} has been updated to {amount} for server {interaction.guild_id}")

        # Send a response message with the updated role pay details
        await interaction.response.send_message(f"Role: {role}\nAmount: {amount}")

    @app_commands.command(name="pay", description="Pay all role pay entries")
    async def pay(self, interaction : Interaction) -> None:
        # Check for admin permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You don't have the required permissions")
            return

        # Checks if role pay entries exist
        rolepay = tables.RolePay.select().where(tables.RolePay.server == interaction.guild_id)
        if not rolepay:
            await interaction.response.send_message("No role pay entries found")
            return

        # Retrieve all role pay entries from the database
        rolepay = tables.RolePay.select().where(tables.RolePay.server == interaction.guild_id)

        for role in rolepay:
            if verbose:
                print(f"Role: {role.role[3:-1]} Amount: {role.amount}")
            # Pay all members with each role
            members = interaction.guild.get_role(int(role.role[3:-1])).members
            if verbose:
                print(f"Members with role {role.role}: {members}")
            
            # Add the role pay amount to each member's balance
            for member in members:
                if verbose:
                    print(f"Member: {member.id}")
                user = tables.Wallet.get_or_none(server=interaction.guild_id, id=member.id)
                if user is None:
                    tables.Wallet.create(server=tables.Server.get_by_id(interaction.guild_id), id=member.id, currency = tables.Currency.select().where(tables.Currency.server == interaction.guild_id).get(), balance=role.amount)
                    if verbose:
                        print(f"Role {role.role} has been paid to {member.id} for server {interaction.guild_id}")
                else:
                    tables.Wallet.update(balance=tables.Wallet.balance + role.amount).where(tables.Wallet.server == interaction.guild_id, tables.Wallet.id == member.id).execute()
                if verbose:
                    print(f"Role {role.role} has been paid to {member.id} for server {interaction.guild_id}")

        # Send a response message with the role pay details
        await interaction.response.send_message("Paying all role pay entries")

async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(RPGroup(name="rp", description="Role Pay Commands"))