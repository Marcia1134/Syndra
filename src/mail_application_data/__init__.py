from discord import Interaction, Embed
from database.tables import Mail
from mail_application_data import create_mail_channel, mark_as_read_toggle, mail_to_embed

async def create_or_get_mail_channel(interaction : Interaction):
    return await create_mail_channel.main(interaction)

async def mail_embed(mail : Mail) -> Embed:
    return await mail_to_embed.main(mail)
# Path: src/mail_application_data/create_mail_channel.py