import discord
import requests

class AddQuoteModal(discord.ui.Modal, title='Add Quote'):
        name = discord.ui.TextInput(
            label='Name',
            placeholder='Who said it?',
        )

        quote = discord.ui.TextInput(
            label='Quote',
            style=discord.TextStyle.long,
            placeholder='Quote...',
            max_length=300,
        )

        async def on_submit(self, interaction: discord.Interaction):
            await interaction.response.send_message(f'Quote added: "{self.quote.value}" -{self.name.value}')
            quote_params = { 'text': self.quote.value, 'person_name': self.name.value }
            requests.post("http://sanctum:8000/quote", json=quote_params)

        async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
            await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
