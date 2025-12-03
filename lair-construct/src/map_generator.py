# This is where the whole map is generated.

import random

import map
import room_generator

class MapGenerator():
    def __init__(self, map_size_x, map_size_y):
        self.map_size_x = map_size_x
        self.map_size_y = map_size_y
        self.map = map.Map(self.map_size_x, self.map_size_y)
        self.rg = room_generator.RoomGenerator()

    def generate(self, seed):
        # Generate a map via a seed
        random.seed(seed)

        # Place initial room
        self.place_initial_room()

        # Choose where the next room goes
        next_room = self.rg.choose_valid_door_tile(self.map)
        self.map = self.rg.place_door(self.map, next_room['door'][0], next_room['door'][1])

        # Loop until target is reached (TODO: TBD)

    def place_initial_room(self):
        room_size_x = random.randint(3, 20)
        room_size_y = random.randint(3, 20)
        room_pos_x = int(self.map_size_x / 2 - room_size_x / 2)
        room_pos_y = int(self.map_size_y / 2 - room_size_y / 2)
        self.rg.build_room(
            pos_x=room_pos_x, 
            pos_y=room_pos_y, 
            size_x=room_size_x, 
            size_y=room_size_y, 
            m=self.map, 
            door_x=-1, 
            door_y=-1
        )

    def place_room(self, pos_x, pos_y, size_x, size_y):
        """ This will attempt to put a room.
        
            Return status:
                1: Yay all is good!
                2: X is too large
                3: Y is too large
                4: X and Y are too large
                5: Confirmed impossible fit
        """
        # See if all the tiles are free

        # If so, change all tiles and return 1

        # If not, then see why... is it x or y? Or both?
        
    def _tiles_free(self, pos_x, pos_y, size_x, size_y):
        for x in range(pos_x, pos_x + size_x):
            for y in range(pos_y, pos_y + size_y):
                tile_value = self.map.get_tile(x, y)
                if tile_value != 0:
                    # We need to see if the room could shrink and fit

                    # If size_x and size_y are at the min values, too bad
                    if size_x == 3 and size_y == 3:
                        return 5
                else:
                    pass
        return 1

