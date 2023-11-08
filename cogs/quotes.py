import discord
from discord import app_commands
from discord.ext import commands
from modals.add_quote_modal import AddQuoteModal

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='add_quote', description='Add and Retrieve Quotes')
    async def add_quote(self, interaction):
        await interaction.response.send_modal(AddQuoteModal())

async def setup(bot):
  await bot.add_cog(Quotes(bot))