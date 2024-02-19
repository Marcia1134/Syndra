import discord
from database.tables import Mail, Transaction
from mail_application_data import mail_to_embed

async def main(mail : Mail, accept_function : function, accept_fuction_args : tuple) -> discord.ui.View:
    class mail_to_view(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            self.mail = mail

        @discord.ui.button(label="Mark as Read", style=discord.ButtonStyle.primary)
        async def mark_as_read(self, button : discord.ui.Button, interaction : discord.Interaction):
            self.mail.read = True
            self.mail.save()
            await interaction.response.edit_message(view=self, embed=await mail_to_embed(self.mail))

        

    return mail_to_view()
