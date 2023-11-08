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
            quote_params = { 'text': self.quote.value }
            response = requests.get("http://127.0.0.1:8000/people/{self.name.value}")

            if response.status_code == 200:
                quote_params['person_id'] = response.json()['id']
            else:
                person_params = { 'name': self.name.value}
                response = requests.post("http://127.0.0.1:8000/people", person_params)
                quote_params['person_id'] = response.json()['id']
                
            requests.post("http://127.0.0.1:8000/quote", )

        async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
            await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
