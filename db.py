import requests, zipfile, os, json, sqlite3
from dotenv import load_dotenv

from model.D2map import Map

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
def get_maps():
    maps = []

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

    for item in item_jsons:
        # 4088006058 is the crucible
        if item['activityTypeHash'] == 4088006058 and item['placeHash'] == 4088006058 and not item['isPvP'] and item['pgcrImage'] != '/img/theme/destiny/bgs/pgcrs/placeholder.jpg':
            newMap = Map(item['originalDisplayProperties']['name'], item['pgcrImage'])
            # check for duplication
            isDupe = False
            for m in maps:
                if m.get_name().__contains__(newMap.get_name()):
                    isDupe = True
            if not isDupe:
                maps.append(newMap)
    return maps
