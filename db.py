import requests, zipfile, os, json, sqlite3
from dotenv import load_dotenv

from model.Map import Map
from model.Weapon import Weapon

load_dotenv()
BUNGIE_API_KEY = os.getenv('BUNGIE_API_KEY')
BASE_URL = 'https://bungie.net/Platform/Destiny2'
BASE_URL_GROUP_V2 = 'https://bungie.net/Platform/GroupV2'


# This code was altered from JAMeador13's code from http://destinydevs.github.io/BungieNetPlatform/docs/Manifest.
# This function downloads Destiny2's database (manifest)
def get_manifest() -> None:
    my_headers = {"X-API-Key": BUNGIE_API_KEY}
    manifest_url = BASE_URL + '/Manifest/'

    # get the manifest location from the json
    r = requests.get(manifest_url, headers=my_headers)
    manifest = r.json()
    mani_url = 'http://www.bungie.net' + manifest['Response']['mobileWorldContentPaths']['en']

    # Download the file, write it to 'MANZIP'
    r = requests.get(mani_url)
    with open("MANZIP", "wb") as zip:
        zip.write(r.content)
    print("Download Complete!")

    # Extract the file contents, and rename the extracted file
    # to 'Manifest.content'
    with zipfile.ZipFile('MANZIP') as zip:
        name = zip.namelist()
        zip.extractall()
    os.rename(name[0], 'Manifest.content')
    print('Unzipped!')


# return a list crucible Map objects
def get_maps(activity_dict: {}) -> tuple[[Map], [Map]]:
    crucible_maps = []
    gambit_maps = []

    place_holder_image = '/img/theme/destiny/bgs/pgcrs/placeholder.jpg'

    for key in activity_dict:
        # Check if the item is a crucible map. 4088006058 is the crucible
        if activity_dict[key]['activityTypeHash'] == 4088006058 and \
                activity_dict[key]['placeHash'] == 4088006058 and not \
                activity_dict[key]['isPvP'] and \
                activity_dict[key]['pgcrImage'] != place_holder_image:

            newMap = Map(activity_dict[key]['originalDisplayProperties']['name'],
                         activity_dict[key]['pgcrImage'],
                         activity_dict[key]['originalDisplayProperties']['description'])

            if not check_for_dupe(newMap, crucible_maps):
                crucible_maps.append(newMap)

        # Check if the item is a gambit map. 248695599 is gambit
        if activity_dict[key]['activityTypeHash'] == 248695599 and \
                activity_dict[key]['placeHash'] == 248695599 and \
                activity_dict[key]['pgcrImage'] != place_holder_image:

            newMap = Map(activity_dict[key]['originalDisplayProperties']['name'],
                         activity_dict[key]['pgcrImage'],
                         activity_dict[key]['originalDisplayProperties']['description'])

            if not check_for_dupe(newMap, gambit_maps):
                gambit_maps.append(newMap)

    return crucible_maps, gambit_maps


# This function checks weather a map list contains a map
def check_for_dupe(new_map: Map, map_list: [Map]) -> bool:
    for m in map_list:
        if m.get_name().__contains__(new_map.get_name()):
            return True
    return False


# This function will return 3 list of weapons
def get_all_weapons(all_data: {}) -> tuple[[Weapon], [Weapon], [Weapon]]:
    kinetic = []
    energy = []
    power = []
    item_def_dict = all_data['DestinyInventoryItemDefinition']
    plug_set_def = all_data['DestinyPlugSetDefinition']
    socket_type_def = all_data['DestinySocketTypeDefinition']

    for key in item_def_dict:
        # itemType 3 is weapon
        if item_def_dict[key]['itemType'] == 3:
            # get the perks for the weapon from all data
            weapon_perks = {}

            for perk_slot in item_def_dict[key]['sockets']['socketEntries']:
                # 4241085061 is weapon perks. If socketTypeHash is 0 means there is not a perk slot there, more common
                # in y1 weapons
                if perk_slot['socketTypeHash'] != 0 and \
                        socket_type_def[perk_slot['socketTypeHash']]['socketCategoryHash'] == 4241085061 and \
                        perk_slot['preventInitializationOnVendorPurchase'] is False:
                    perk_pool = []

                    # randomizedPlugSetHash signals that this weapon do or don't have random rolls
                    if 'randomizedPlugSetHash' in perk_slot:
                        # Go to PlugSetDef to grab the list of perks for random rolls
                        for perk in plug_set_def[perk_slot['randomizedPlugSetHash']]['reusablePlugItems']:
                            perk_pool.append(item_def_dict[perk['plugItemHash']]['displayProperties']['name'])

                    elif perk_slot['singleInitialItemHash'] != 0:
                        # Just go grab the perk name from InvItemDef based on the perk hash
                        perk_pool.append(item_def_dict[perk_slot['singleInitialItemHash']]['displayProperties']['name'])

                    perk_type = socket_type_def[perk_slot['socketTypeHash']]['plugWhitelist'][0]['categoryIdentifier']

                    # check if key already exists
                    if perk_type in weapon_perks:
                        perk_type += ' '

                    weapon_perks[perk_type] = perk_pool

            # create the weapon obj
            current_weapon = Weapon(
                key,
                item_def_dict[key]['displayProperties']['name'],
                item_def_dict[key]['screenshot'],
                item_def_dict[key]['displayProperties']['icon'],
                item_def_dict[key]['itemTypeDisplayName'],
                item_def_dict[key]['inventory']['tierTypeName'],
                weapon_perks
            )

            # itemCategoryHashes 3 = energy, 2 = kinetic, 4 = power
            if item_def_dict[key]['itemCategoryHashes'][0] == 3:
                energy.append(current_weapon)
            elif item_def_dict[key]['itemCategoryHashes'][0] == 2:
                kinetic.append(current_weapon)
            elif item_def_dict[key]['itemCategoryHashes'][0] == 4:
                power.append(current_weapon)

    return kinetic, energy, power


# This function will return the list of all weapon perks
def get_all_weapon_perks(all_data: {}) -> [str]:
    item_def_dict = all_data['DestinyInventoryItemDefinition']
    perks = [str]
    for key in item_def_dict:
        # 3708671066 is frame
        # 3085181971 is barrel
        # 4184407433 is magazines
        # 2411768833 is scopes
        # itemType 19 is Mods
        if item_def_dict[key]['displayProperties']['name'] != '' and \
                item_def_dict[key]['itemType'] == 19 and (
                        3708671066 in item_def_dict[key]['itemCategoryHashes'] or
                        3085181971 in item_def_dict[key]['itemCategoryHashes'] or
                        4184407433 in item_def_dict[key]['itemCategoryHashes'] or
                        2411768833 in item_def_dict[key]['itemCategoryHashes']
                ):
            perks.append(item_def_dict[key]['displayProperties']['name'])
    return perks


# This function will return the hash table of the manifest
def built_dict(hash_dict: {}) -> {}:
    # connect to the manifest
    con = sqlite3.connect('manifest.content')
    print('Connected')
    # create a cursor object
    cur = con.cursor()

    all_data = {}

    for table_name in hash_dict:
        # get a list of all jsons from the DestinyActivityDefinition
        cur.execute('SELECT json from ' + table_name)
        print('Generating ' + table_name + ' dictionary....')

        # this returns a list of tuples: the first item in each tuple is our json
        items = cur.fetchall()

        # create a lists of jsons
        item_jsons = [json.loads(item[0]) for item in items]

        # Create a dictionary with the hashes as keys and the jsons as values
        item_dict = {}
        key = hash_dict[table_name]
        for item in item_jsons:
            item_dict[item[key]] = item

        # Add that dictionary to our all_data using the name of the table as a key.
        all_data[table_name] = item_dict

    print('Dictionary Generated!')
    return all_data
