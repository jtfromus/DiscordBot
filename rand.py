from db import get_maps
from model.D2map import Map
import random


# This function returns a string of the random map chosen
def chose_rand_map():
    # If the maps list is exhausted reset it
    if not D2Maps.maps:
        D2Maps.maps = D2Maps.used_maps
        D2Maps.used_maps = []

    # Chose a random map
    currentMap = random.choice(D2Maps.maps)
    D2Maps.maps.remove(currentMap)
    D2Maps.used_maps.append(currentMap)

    return currentMap.getName()


# Temp solution for having a list of maps
class D2Maps:
    used_maps = []
    maps = []
    # add all the maps to a list
    map_names = get_maps()
    for name in map_names:
        maps.append(Map(name))
