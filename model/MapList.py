import random
from model.Map import Map


class MapList:
    def __init__(self, maps):
        self.used_maps = []
        self.maps = maps
        print(str(len(self.maps)) + " maps loaded")

    # This function returns a random map object
    def chose_rand_map(self) -> Map:
        # If the maps list is exhausted reset it
        if not self.maps:
            print('list exhausted')
            self.maps = self.used_maps
            self.used_maps = []

        # Chose a random map
        currentMap = random.choice(self.maps)
        self.maps.remove(currentMap)
        self.used_maps.append(currentMap)

        return currentMap

    # reset the list from database
    def reset_maps(self, maps: [Map]) -> None:
        self.used_maps = []
        self.maps = maps

    def get_maps(self) -> [Map]:
        return self.maps
