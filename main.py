import os
import pickle

import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from dotenv import load_dotenv

import db
from rand import chose_rand_map

load_dotenv()
DISCORD_TOKEN = os.getenv('TOKEN')
TEST_SERVER_ID = os.getenv('DS_TEST_SERVER_ID')
bot = commands.Bot(command_prefix='~')
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has joined Discord!')


# Slash command
@slash.slash(
    name='rand',
    description="This function will give you a randomized choice out of each option category",
    guild_ids=[int(TEST_SERVER_ID)],
    options=[
        create_option(
            name="option",
            description="chose what to be random",
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name="map",
                    value="m"
                )
            ]
        )
    ]
)
async def _rand_map(ctx: SlashContext, option: str):
    if option == 'm':
        await ctx.send(chose_rand_map())


@slash.slash(
    name='updateDB',
    description="This function will update the database from bungie",
    guild_ids=[int(TEST_SERVER_ID)],
)
async def _rand_map(ctx: SlashContext):
    await ctx.send(db.get_manifest())


# Bot chat
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('SSlave'):
        await message.channel.send('SSlave sees you...')
    await bot.process_commands(message)


# Text channel commands
@bot.command()
async def rand(ctx, *args):
    for arg in args:
        if arg == '-m':
            await ctx.send(chose_rand_map())


# check if pickle exists, if not create one.
if not os.path.isfile(r'manifest.content'):
    db.get_manifest()
else:
    print('DB Exists')

bot.run(DISCORD_TOKEN)
