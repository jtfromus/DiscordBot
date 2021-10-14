import requests, zipfile, os, json, sqlite3
from dotenv import load_dotenv

from model.Map import Map
from model.Weapon import Weapon

load_dotenv()
BUNGIE_API_KEY = os.getenv('BUNGIE_API_KEY')
BASE_URL = 'https://bungie.net/Platform/Destiny2'
BASE_URL_GROUP_V2 = 'https://bungie.net/Platform/GroupV2'


# This code was altered from JAMeador13's code from http://destinydevs.github.io/BungieNetPlatform/docs/Manifest.
def get_manifest():
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
def get_maps() -> tuple[[Map], [Map]]:
    crucible_maps = []
    gambit_maps = []

    # connect to the manifest
    con = sqlite3.connect('manifest.content')
    print('Connected')
    # create a cursor object
    cur = con.cursor()

    # get a list of all jsons from the DestinyActivityDefinition
    cur.execute('SELECT json from DestinyActivityDefinition')

    # this returns a list of tuples: the first item in each tuple is our json
    items = cur.fetchall()

    # create a list of jsons
    item_jsons = [json.loads(item[0]) for item in items]

    place_holder_image = '/img/theme/destiny/bgs/pgcrs/placeholder.jpg'

    for item in item_jsons:
        # Check if the item is a crucible map. 4088006058 is the crucible
        if item['activityTypeHash'] == 4088006058 and \
                item['placeHash'] == 4088006058 and not \
                item['isPvP'] and \
                item['pgcrImage'] != place_holder_image:
            
            newMap = Map(item['originalDisplayProperties']['name'], 
                         item['pgcrImage'],
                         item['originalDisplayProperties']['description'])
            
            if not check_for_dupe(newMap, crucible_maps):
                crucible_maps.append(newMap)

        # Check if the item is a gambit map. 248695599 is gambit
        if item['activityTypeHash'] == 248695599 and \
                item['placeHash'] == 248695599 and \
                item['pgcrImage'] != place_holder_image:
            
            newMap = Map(item['originalDisplayProperties']['name'], 
                         item['pgcrImage'],
                         item['originalDisplayProperties']['description'])
            
            if not check_for_dupe(newMap, gambit_maps):
                gambit_maps.append(newMap)

    con.close()
    print('Connection Closed')
    return crucible_maps, gambit_maps


# This function checks weather a map list contains a map
def check_for_dupe(new_map: Map, map_list: [Map]) -> bool:
    for m in map_list:
        if m.get_name().__contains__(new_map.get_name()):
            return True
    return False


# This function will return 3 list of weapons
def get_all_weapons() -> tuple[[Weapon], [Weapon], [Weapon]]:
    # connect to the manifest
    con = sqlite3.connect('manifest.content')
    print('Connected')
    # create a cursor object
    cur = con.cursor()
    # get a list of all jsons from the DestinyActivityDefinition
    cur.execute('SELECT json from DestinyInventoryItemDefinition')

    # this returns a list of tuples: the first item in each tuple is our json
    items = cur.fetchall()

    # create a lists of jsons
    item_jsons = [json.loads(item[0]) for item in items]

    kinetic = []
    energy = []
    power = []

    for item in item_jsons:
        # itemType 3 is weapon
        if item['itemType'] == 3:
            current_weapon = Weapon(
                item['displayProperties']['name'],
                item['screenshot'],
                item['itemTypeDisplayName'],
                item['inventory']['tierTypeName']
            )
            
            # itemCategoryHashes 3 = energy, 2 = kinetic, 4 = power
            if item['itemCategoryHashes'][0] == 3:
                energy.append(current_weapon)
            elif item['itemCategoryHashes'][0] == 2:
                kinetic.append(current_weapon)
            elif item['itemCategoryHashes'][0] == 4:
                power.append(current_weapon)

    con.close()
    print('Connection Closed')
    return kinetic, energy, power
