import os
import discord
import db

from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from dotenv import load_dotenv
from rand import reset_maps, chose_rand_map

load_dotenv()
DISCORD_TOKEN = os.getenv('TOKEN')
TEST_SERVER_ID = os.getenv('DS_TEST_SERVER_ID')
SERVER_ID = os.getenv('SERVER_ID')
BUNGIE_URL = os.getenv('BUNGIE_URL')
bot = commands.Bot(command_prefix='~')
slash = SlashCommand(bot, sync_commands=True)

# check if pickle exists, if not create one.
if not os.path.isfile(r'manifest.content'):
    db.get_manifest()
else:
    print('DB Exists')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has joined Discord!')


# Slash command
@slash.slash(
    name='rand',
    description="This function will give you a randomized choice out of each option category",
    guild_ids=[int(TEST_SERVER_ID),int(SERVER_ID)],
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
        chosen_map = chose_rand_map()
        embed = discord.Embed(title=chosen_map.get_name(),
                              url=BUNGIE_URL + chosen_map.get_image_url(),
                              description=chosen_map.get_description(),
                              color=0xFF5733)
        embed.set_thumbnail(url='https://www.bungie.net/common/destiny2_content/icons/DestinyActivityModeDefinition_5b371fef4ecafe733ad487a8fae3b9f5.png')
        embed.set_image(url=BUNGIE_URL + chosen_map.get_image_url())
        await ctx.send(embed=embed)


@slash.slash(
    name='updateDB',
    description="This function will update the database from bungie",
    guild_ids=[int(TEST_SERVER_ID),int(SERVER_ID)],
)
async def _rand_map(ctx: SlashContext):
    db.get_manifest()
    reset_maps()
    await ctx.send('Database is updated')


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
            await ctx.send(rand.chose_rand_map())

bot.run(DISCORD_TOKEN)
