import os
import discord
import requests
import json

from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
DISCORD_TOKEN = os.getenv('TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix='~')

"""
def get_map():
    response = requests.get("https://")
    jsonData = json.loads(response.text)
    map = jsonData[][] + " -"
    return(map)
"""


@bot.event
async def on_ready():
    print(f'{bot.user.name} has joined Discord!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('SSlave'):
        await message.channel.send('SSlave sees you...')
    await bot.process_commands(message)


print("TOKEN: " + DISCORD_TOKEN)


@bot.command()
async def random(ctx, *args):
    print('random is called')
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))


bot.run(DISCORD_TOKEN)
