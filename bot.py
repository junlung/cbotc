import discord
import os
import asyncio
import json
from modals.add_member_modal import AddMemberModal
from discord.ext.commands import Context
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

import sys
sys.path.append('../')

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
mtg_channel_id = int(os.getenv('MTG_CHANNEL_ID'))
guild_id = os.getenv('GUILD_ID')

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
  channel = bot.get_channel(mtg_channel_id)
  changelog = get_latest_changelog()
  current_version = get_current_version()

  if current_version != changelog['number']:
    update_version(changelog['number'])
    changes = map(lambda c: '- ' + c, changelog['changes'])
    message =  f"**CBot Running on Version ({changelog['number']})**: \n" + '\n'.join(changes)
    await channel.send(message)
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

def get_latest_changelog():
  with open('/app/data/changelogs.json', 'r') as file:
    changelogs = json.load(file)
    return changelogs['versions'][-1]

def get_current_version():
  try:
    with open('/app/data/version.txt', 'r') as file:
      return file.read().strip()
  except FileNotFoundError:
    return "0.0.0"
  
def update_version(new_version):
  with open('/app/data/version.txt', 'w') as file:
    file.write(new_version)

asyncio.run(main())