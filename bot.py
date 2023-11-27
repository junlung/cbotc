import discord
import os
import asyncio
from modals.add_member_modal import AddMemberModal
from discord.ext.commands import Context
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

import sys
sys.path.append('../')

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def sync(ctx: Context):
    ctx.bot.tree.copy_global_to(guild=ctx.guild)
    await ctx.bot.tree.sync(guild=ctx.guild)

async def load_cogs():
    await bot.load_extension('cogs.mtg')
    await bot.load_extension('cogs.quotes')

@bot.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(bot))
    #await tree.sync(guild=discord.Object(id=1170197562947543060))

@app_commands.context_menu(name="Add Discord Member")
async def add_member(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_modal(AddMemberModal(username=user.display_name, user_id=user.id))

async def main():
    async with bot:
        await load_cogs()
        bot.tree.add_command(add_member)
        bot.tree.copy_global_to(guild=discord.Object(id=1170197562947543060))
        bot.tree.copy_global_to(guild=discord.Object(id=732274969546981441))
        await bot.start(token)

asyncio.run(main())