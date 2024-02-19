import discord
from database.tables import MailChannel

async def main(interaction : discord.Interaction):
    server = interaction.guild
    syndra_category = discord.utils.get(server.categories, name="Syndra")
    if syndra_category is None:
        syndra_category = await server.create_category_channel("Syndra")
    if MailChannel.get_or_none(MailChannel.recipient == interaction.user.id) is None:
        mail_channel = await server.create_text_channel("mail", category=syndra_category)
        MailChannel.create(recipient=interaction.user.id, server=server.id, channel=mail_channel.id)
        await mail_channel.send("Welcome to the mail channel! Here you can send and receive mail from other members of the server.")
    else:
        mail_channel = discord.utils.get(syndra_category.text_channels, name="mail")

    return mail_channel