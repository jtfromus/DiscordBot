import os
import discord
import db

from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from dotenv import load_dotenv
from model.MapList import MapList

# load env infos
load_dotenv()
DISCORD_TOKEN = os.getenv('TOKEN')
TEST_SERVER_ID = os.getenv('DS_TEST_SERVER_ID')
SERVER_ID = os.getenv('SERVER_ID')
BUNGIE_URL = os.getenv('BUNGIE_URL')

# bot command settings
bot = commands.Bot(command_prefix='~')
slash = SlashCommand(bot, sync_commands=True)

# check if db exists, if not create one.
if not os.path.isfile(r'manifest.content'):
    db.get_manifest()
else:
    print('DB Exists')

# set up the lists
cl, gl = db.get_maps()
gambit_list = MapList(gl)
crucible_list = MapList(cl)


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
                    name="crucible",
                    value="c"
                ),
                create_choice(
                    name="gambit",
                    value="g"
                )
            ]
        )
    ]
)
async def _rand_map(ctx: SlashContext, option: str):
    if option == 'c':
        chosen_map = crucible_list.chose_rand_map()
        thumbnail = 'https://www.bungie.net/common/destiny2_content/icons/DestinyActivityModeDefinition_5b371fef4ecafe733ad487a8fae3b9f5.png'
    elif option == 'g':
        chosen_map = gambit_list.chose_rand_map()
        thumbnail = 'https://www.bungie.net/common/destiny2_content/icons/DestinyActivityModeDefinition_96f7e9009d4f26e30cfd60564021925e.png'

    embed = discord.Embed(title=chosen_map.get_name(),
                          url=BUNGIE_URL + chosen_map.get_image_url(),
                          description=chosen_map.get_description(),
                          color=0xFF5733)
    embed.set_thumbnail(url=thumbnail)
    embed.set_image(url=BUNGIE_URL + chosen_map.get_image_url())
    await ctx.send(embed=embed)


@slash.slash(
    name='updateDB',
    description="This function will update the database from bungie",
    guild_ids=[int(TEST_SERVER_ID),int(SERVER_ID)],
)
async def _update_db(ctx: SlashContext):
    db.get_manifest()
    c, g = db.get_maps()
    gambit_list.reset_maps(g)
    crucible_list.reset_maps(c)
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
