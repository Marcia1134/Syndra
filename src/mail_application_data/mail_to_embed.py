import discord
from database.tables import Mail, Transaction

async def main(mail : Mail) -> discord.Embed:
    mail_embed = discord.Embed(title="Mail")
    transaction : Transaction = mail.transaction
    
    if mail.read:
        mail_embed.color = discord.Color.green()
        mail_embed.set_footer(text="Read ✅")
    else:
        mail_embed.color = discord.Color.red()
        mail_embed.set_footer(text="Unread ❌")

    mail_embed.add_field(name="From", value=f"<@{transaction.sender}>")
    mail_embed.add_field(name="Amount", value=transaction.amount)
    mail_embed.add_field(name="Date", value=transaction.date)
    mail_embed.add_field(name="Description", value=transaction.description)

    return mail_embed