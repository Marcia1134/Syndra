from discord import app_commands, Interaction
from discord.ext import commands
from database.tables import Mail
from mail_application_data import create_or_get_mail_channel, mail_to_embed

class MailGroup(app_commands.Group):

    @app_commands.command(name="get", description="List all mail entries")
    async def list(self, interaction : Interaction) -> None:
        mail_channel = create_or_get_mail_channel(interaction)
        # Retrieve all mail entries from the database
        mail = Mail.select().where(Mail.recipient == interaction.user.id)
        
        # Send a response message with the mail details
        for entry in mail:
            await mail_channel.send(embed=await mail_to_embed(entry))

        # Send a response message with the mail details
        await interaction.response.send_message(f"Your Mail has been sent! {mail_channel}", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_command(MailGroup(bot))