import os
import random

import discord
import db
import re

from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from dotenv import load_dotenv

from model import Weapon
from model.MapList import MapList


def main(args=None):
    # load env infos
    load_dotenv()
    DISCORD_TOKEN = os.getenv('TOKEN')
    TEST_SERVER_ID = os.getenv('DS_TEST_SERVER_ID')
    SERVER_ID = os.getenv('SERVER_ID')
    BUNGIE_URL = os.getenv('BUNGIE_URL')
    GUILD_ID_LIST = [int(TEST_SERVER_ID), int(SERVER_ID)]

    hashes = {
        'DestinyActivityDefinition': 'hash',
        'DestinyInventoryItemDefinition': 'hash',
        'DestinyPlugSetDefinition': 'hash',
        'DestinySocketTypeDefinition': 'hash'
    }

    # bot command settings
    bot = commands.Bot(command_prefix='~')
    slash = SlashCommand(bot, sync_commands=True)

    # check if db exists, if not create one.
    if not os.path.isfile(r'manifest.content'):
        db.get_manifest()
    else:
        print('DB Exists')

    # Put all the info into all_data
    all_data = db.built_dict(hashes)

    # set up the lists
    cl, gl = db.get_maps(all_data['DestinyActivityDefinition'])
    gambit_list = MapList(gl)
    crucible_list = MapList(cl)
    kinetic, energy, power = db.get_all_weapons(all_data)

    @bot.event
    async def on_ready() -> None:
        print(f'{bot.user.name} has joined Discord!')

    # Slash command
    @slash.slash(
        name='rand',
        description="This function will give you a randomized choice out of each option category",
        guild_ids=GUILD_ID_LIST,
        options=[
            create_option(
                name="playlist",
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
            ),
            create_option(
                name="weapon",
                description="generate random weapon types",
                required=False,
                option_type=5
            )
        ]
    )
    async def _rand(ctx: SlashContext, playlist: str, weapon: bool = None) -> None:
        if playlist == 'c':
            chosen_map = crucible_list.chose_rand_map()
            thumbnail = 'https://www.bungie.net/common/destiny2_content/icons/DestinyActivityModeDefinition_5b371fef4ecafe733ad487a8fae3b9f5.png'
        elif playlist == 'g':
            chosen_map = gambit_list.chose_rand_map()
            thumbnail = 'https://www.bungie.net/common/destiny2_content/icons/DestinyActivityModeDefinition_96f7e9009d4f26e30cfd60564021925e.png'

        embed = discord.Embed(title=chosen_map.get_name(),
                              url=BUNGIE_URL + chosen_map.get_image_url(),
                              description=chosen_map.get_description(),
                              color=0xFF5733)
        embed.set_thumbnail(url=thumbnail)
        embed.set_image(url=BUNGIE_URL + chosen_map.get_image_url())

        if weapon is not None and weapon:
            kin = random.choice(kinetic)
            embed.add_field(name='Kinetic', value=kin.get_weapon_type(), inline=True)
            ene = random.choice(energy)
            embed.add_field(name='Energy', value=ene.get_weapon_type(), inline=True)
            heavy = random.choice(power)
            embed.add_field(name='Power', value=heavy.get_weapon_type(), inline=True)

        await ctx.send(embed=embed)

    @slash.slash(
        name='dice_rolls',
        description="This function return a random dice roll for you ;)",
        guild_ids=GUILD_ID_LIST,
        options=[
            create_option(
                name="value",
                description="<int>d<int> ex: 2d4",
                required=True,
                option_type=3
            )
        ]
    )
    async def _dice_roll(ctx: SlashContext, value: str) -> None:
        # pattern for input validation
        pattern = '^[1-9]\d*d[1-9]\d*$'
        result = []
        total = 0

        if re.match(pattern, value):
            # split the two numbers
            dice = value.split('d')

            # roll the dice
            for x in range(int(dice[0])):
                v = random.randint(1, int(dice[1]))
                total += v
                result.append(str(v))

            result_str = f"Total: {str(total)}\nRoll result: \n{' | '.join(result)}"
            embed = discord.Embed(title=value,
                                  description=result_str,
                                  color=0xFF5733)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='ERROR',
                                  description=f'You entered an invalid value: {value}\n'
                                              f'it should\'ve been <int>d<int> and int > 0',
                                  color=0xFF5733)
            await ctx.send(embed=embed)

    @slash.slash(
        name='updateDB',
        description="This function will update the database from bungie, and refresh the lists for the bot",
        guild_ids=GUILD_ID_LIST,
    )
    async def _update_db(ctx: SlashContext) -> None:
        await ctx.defer()
        db.get_manifest()

        # Put all the info into all_data
        global all_data
        all_data = db.built_dict(hashes)

        c, g = db.get_maps(all_data['DestinyActivityDefinition'])
        gambit_list.reset_maps(g)
        crucible_list.reset_maps(c)
        global kinetic, energy, power
        kinetic, energy, power = db.get_all_weapons(all_data['DestinyInventoryItemDefinition'])

        await ctx.send('Database is updated')

    @slash.slash(
        name='get_weapon_rolls',
        description="This function gives you the perk roll a gun can drop",
        guild_ids=GUILD_ID_LIST,
        options=[
            create_option(
                name="name",
                description="name of the gun",
                required=True,
                option_type=3
            )
        ]
    )
    async def _weapon_rolls(ctx: SlashContext, name: str) -> None:
        weapon: Weapon
        # See if the weapon exists
        weapon = Weapon.find_weapon(kinetic + energy + power, name)

        if weapon is None:
            embed = discord.Embed(title='WEAPON NOT FOUND',
                                  description=f'{name} is not found\n'
                                              f'please check if the weapon name is correct',
                                  color=0xFF5733)
        else:
            # Prepare the embedded message
            embed = discord.Embed(title=weapon.get_name(),
                                  description=weapon.get_weapon_type(),
                                  color=0xFF5733)
            embed.set_thumbnail(url=BUNGIE_URL + weapon.get_icon())
            for key in weapon.get_perks():
                embed.add_field(name=key, value=',\n'.join(weapon.get_perks()[key]), inline=True)
        await ctx.send(embed=embed)

    # Bot chat
    @bot.event
    async def on_message(message) -> None:
        if message.author == bot.user:
            return

        if message.content.startswith('SSlave'):
            await message.channel.send('SSlave sees you...')
        await bot.process_commands(message)

    # Text channel commands
    @bot.command()
    async def rand(ctx, *args) -> None:
        for arg in args:
            if arg == '-m':
                await ctx.send(rand.chose_rand_map())

    bot.run(DISCORD_TOKEN)


if __name__ == '__main__':
    main()
