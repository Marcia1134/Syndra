from discord import app_commands, Interaction
from discord.ext import commands
from database.tables import Mail

class MailGroup(app_commands.Group):

    @app_commands.command(name="list", description="List all mail entries")
    async def list(self, interaction : Interaction) -> None:
        # Retrieve all mail entries from the database
        mail = Mail.select().where(Mail.recipient == interaction.user.id)
        mail_list = ""
        for m in mail:
            mail_list += f"Mail: {m.mail}\n"
        if mail_list == "":
            mail_list = "No mail entries found"

        # Send a response message with the mail details
        await interaction.response.send_message(mail_list, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_command(MailGroup(bot))