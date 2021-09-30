import random

# This function returns a string of the random map chosen
from db import get_maps

class D2Maps:
    used_maps = []
    # add all the maps to a list
    maps = get_maps()

def chose_rand_map():
    # If the maps list is exhausted reset it
    if not D2Maps.maps:
        D2Maps.maps = D2Maps.used_maps
        D2Maps.used_maps = []

    # Chose a random map
    currentMap = random.choice(D2Maps.maps)
    D2Maps.maps.remove(currentMap)
    D2Maps.used_maps.append(currentMap)

    return currentMap


def reset_maps():
    D2Maps.used_maps = []
    D2Maps.maps = get_maps()
