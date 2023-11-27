import discord
import requests

class AddMemberModal(discord.ui.Modal):
    name = discord.ui.TextInput(
        label='Name'
    )

    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        super().__init__(title='Add Member')

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Member added!", ephemeral=True)
        member_params = {
            'name': self.name.value,
            'discord_id': self.user_id,
            'discord_username': self.username
        }
        requests.post("http://sanctum:8000/discord_members", json=member_params)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
