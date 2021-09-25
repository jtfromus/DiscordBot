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
    # add all the maps to a list
    maps = [Map("Alter of Flames"),
            Map("Anomaly"),
            Map("Bannerfall"),
            Map("The Burnout"),
            Map("Cauldron"),
            Map("Convergence"),
            Map("Dead Cliffs"),
            Map("Distant Shore"),
            Map("Endless Vail"),
            Map("Exdous Blue"),
            Map("The Fortress"),
            Map("Fragment"),
            Map("Javelin-4"),
            Map("Midtown"),
            Map("Pacifica"),
            Map("Radiant Cliffs"),
            Map("Rusted Lands"),
            Map("Twilight Gap"),
            Map("Widow's Court"),
            Map("Warmhaven")]
