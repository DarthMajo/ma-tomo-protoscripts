# This is where the whole map is generated.

import random

import map

class MapGenerator():
    def __init__(self, map_size_x, map_size_y):
        self.map_size_x = map_size_x
        self.map_size_y = map_size_y
        self.map = map.Map(self.map_size_x, self.map_size_y)

    def generate(self, seed):
        # Generate a map via a seed
        random.seed(seed)

        # Place initial room
        room_size_x = random.randint(3, 20)
        room_size_y = random.randint(3, 20)
        room_pos_x = map_size_x / 2 - room_size_x / 2
        room_pos_y = map_size_y / 2 - room_size_y / 2

        

        # Loop until target is reached (TODO: TBD)

    def place_room(self):
        # This will attempt to put a room.
        pass

