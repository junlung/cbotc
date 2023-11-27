import discord
import requests
from discord import app_commands
from discord.ext import commands
from modals.add_quote_modal import AddQuoteModal

class Quotes(commands.Cog):
    """ A Cog that allows quotes to be logged to Sanctum """
    def __init__(self, bot):
        self.bot = bot
        self.add_quote_ctx = app_commands.ContextMenu(
            name="Add Quote",
            callback = self.add_quote_from_message
        )
        self.bot.tree.add_command(self.add_quote_ctx)

    @app_commands.command(name='add_quote', description='Add and Retrieve Quotes')
    async def add_quote(self, interaction):
        await interaction.response.send_modal(AddQuoteModal())

    async def add_quote_from_message(self, interaction: discord.Interaction, message: discord.Message):
        params = {
            'person_discord_id': message.author.id,
            'text': message.content
        }
        requests.post("http://sanctum:8000/quote", json=params)
        await interaction.response.send_message("Quote added!")

async def setup(bot):
  await bot.add_cog(Quotes(bot))