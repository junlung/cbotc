import requests
import discord
import aiohttp
from io import BytesIO
from discord import app_commands, Embed, Color
from embeds import CardFinder
from discord.ext import commands

class Mtg(commands.Cog):
  #############################
  ##   INITIALIZATION
  #############################
  def __init__(self, bot):
    self.bot = bot

  async def cog_unload(self):
    self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

  #############################
  ##   COMMANDS
  #############################
  @app_commands.command(name='card')
  @app_commands.describe(name='The name of the card to search')
  async def card(self, interaction: discord.Interaction, name: str):
    """ Search for a card on Scryfall """
    print("looking for " + name)
    response = requests.get(name_to_url(name))

    if response.status_code == 200:
      print(response.json()['image_uris']['png'])
      image = response.json()['image_uris']['png']
      await interaction.response.send_message(image)
    else:
      print("not found")
      await interaction.response.send("Card not found!")

  @commands.Cog.listener()
  async def on_message(self, message):
    card_embeds = []
    cards = get_cards_from_message(message.content)
    for card in cards:
      print(card)
      print(embed_from_card(card))
      card_embeds.append(embed_from_card(card))
    await message.channel.send(embeds=card_embeds)

#############################
##   HELPER METHODS
#############################
def get_cards_from_message(content: str):
  """
  checks a message for card names and returns card data

  :param content: the String to search
  :return: a List of Dicts with card info
  """ 
  cards = []
  names = get_card_names_from_text(content)
  print(names)
  for name in names:
    url = get_url_from_name(name)
    print(url)
    card = get_card_data(url)
    print(card)
    if card != None: cards.append(card)
  return cards

def get_card_names_from_text(content: str):
  """
  finds and returns all text in [[]]

  :param content: the String to search
  :return: a List of Strings found within [[]]
  """ 
  names = []
  chunks = content.split("[[")

  for c in chunks[1:]:
    name = c.split("]]")
    if len(name) > 1: names.append(name[0]) 

  return names

def get_url_from_name(name: str):
  """
  converts a card name to a scryfall query url

  :param name: the card name
  :return: a scryfall query url
  """ 
  url_base = "https://api.scryfall.com/cards/named?fuzzy="
  return url_base + name.replace(" ", "+")

def get_card_data(url: str):
  """
  queries for a card and returns relevant info

  :param url: the url to send to scryfall
  :return: an object containing useful card info
  """ 
  response = requests.get(url)
  if response.status_code != 200: return None

  data = response.json()
  card = {
    "id":         data['id'],
    "url":        data['scryfall_uri'],
    "name":       data['name'],
    "image":      data['image_uris']['png'],
    "mana_cost":  data['mana_cost'],
    "cmc":        data['cmc'],
    "type":       data['type_line'],
    "text":       data['oracle_text'],
    "colors":     data['colors'],
    "rarity":     data['rarity']
  }

  if 'power' in data: card.update(
    {
      "power":      data['power'],
      "toughness":  data['toughness']
    }
  )
    
  return card

def embed_from_card(card: dict):
  """
  creates an embed from card info

  :param card: a dict of card info
  :return: an Embed of the card info
  """ 
  colors = {
    "W": 0xf8e7b9,
    "U": 0x0e67ab,
    "B": 0x150b00,
    "R": 0xd3202a,
    "G": 0x00733d,
  }

  description = f'{card["type"]}\n{card["text"]}'
  if 'power' in card: description += f'\n{card["power"]}/{card["toughness"]}'

  print(description)
  color = 0x969696
  if len(card['colors']) > 0: color = colors[card['colors'][0]]

  params = {
    "color": color,
    "title": card['name'],
    "url": card['url'],
    "description": description
  }

  embed = Embed(**params)
  embed.set_thumbnail(url=card['image'])
  print(embed)
  return embed

def name_to_url(text):
  search = "https://api.scryfall.com/cards/named?fuzzy="
  search += text.replace(" ", "+")

  return search

def get_card_image(name):
  response = requests.get(name_to_url(name))
  if response.status_code == 200:
    return response.json()['image_uris']['png']
  else:
    print("not found")


async def setup(bot):
  await bot.add_cog(Mtg(bot))