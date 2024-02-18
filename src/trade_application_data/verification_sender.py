from discord import Interaction, Embed, ui, User, ButtonStyle
from database import tables
from trade_application_data.verification_reciever import VerificationReciever, VerificationRecieverEmbed

class VerificationSender(ui.View):
    def __init__(self, user: User, amount: int, interaction : Interaction, wallet_sender : tables.Wallet, wallet_reciver : tables.Wallet) -> None:
        super().__init__()
        self.user = user
        self.amount = amount
        self.interaction = interaction
        self.wallet_sender = wallet_sender
        self.wallet_reciver = wallet_reciver

    @ui.button(label="Accept", style=ButtonStyle.success, emoji="✅")
    async def accept(self, interaction : Interaction, button : ui.button) -> None:
        await interaction.response.send_message(embed=VerificationRecieverEmbed(self.user, self.amount, self.wallet_reciver), view=VerificationReciever(self.user, self.amount, interaction, self.wallet_sender, self.wallet_reciver))

    @ui.button(label="Decline", style=ButtonStyle.danger, emoji="❌")
    async def decline(self, interaction : Interaction, button : ui.button) -> None:
        await interaction.response.send_message("Trade declined", ephemeral=True)
        await interaction.message.delete()
        if self.bot.verbose:
            print("Trade declined")

def VerificationSenderEmbed(user : User, amount : int, wallet : tables.Wallet) -> Embed:
    embed = Embed(title="Trade verification", description=f"{user.mention} wants to trade {amount} {tables.Currency.select().where(tables.Currency.id == wallet.currency).get().symbol} with you")

    return embed