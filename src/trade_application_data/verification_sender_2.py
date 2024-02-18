from discord import Interaction, Embed, ui, User, ButtonStyle
from database import tables

class VerificationSender(ui.View):
    def __init__(self, user: User, amount: int, interaction : Interaction, wallet_sender : tables.Wallet, wallet_reciver : tables.Wallet) -> None:
        super().__init__()
        self.user = user
        self.amount = amount
        self.interaction = interaction
        self.wallet_sender : tables.Wallet = wallet_sender
        self.wallet_reciver : tables.Wallet = wallet_reciver

    @ui.button(label="Accept", style=ButtonStyle.success, emoji="✅")
    async def accept(self, interaction : Interaction, button : ui.button) -> None:
        self.wallet_sender.balance -= self.amount
        self.wallet_sender.save()

        self.wallet_reciver.balance += self.amount
        self.wallet_reciver.save()

        await interaction.response.send_message("Trade accepted", ephemeral=True)
        await interaction.message.delete()
        if self.bot.verbose:
            print("Trade accepted")

    @ui.button(label="Decline", style=ButtonStyle.danger, emoji="❌")
    async def decline(self, interaction : Interaction, button : ui.button) -> None:
        await interaction.response.send_message("Trade declined", ephemeral=True)
        await interaction.message.delete()
        if self.bot.verbose:
            print("Trade declined")

def VerificationSenderEmbed(user : User, amount : int, wallet : tables.Wallet) -> Embed:
    embed = Embed(title="Trade verification", description=f"{user.mention} wants to trade {amount} {tables.Currency.select().where(tables.Currency.id == wallet.currency).get().symbol} with you")

    return embed
