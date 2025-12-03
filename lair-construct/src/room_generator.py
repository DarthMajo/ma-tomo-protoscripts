# This will create the individual room in a map

import random

class RoomGenerator():
    def __init__(self):
        pass

    def build_room(self, pos_x, pos_y, size_x, size_y, m, door_x, door_y):
        # Builds a room of x and y size on map m
        # The door location is where the origin of the room will begin
        for x in range(pos_x, pos_x + size_x):
            for y in range(pos_y, pos_y + size_y):
                if x == door_x and y == door_y:
                    m.set_tile(x, y, 68)
                if self._should_be_wall_tile(pos_x, pos_y, size_x, size_y, x, y):
                    m.set_tile(x, y, 88)
                else:
                    m.set_tile(x, y, 46)
        return m
    
    def choose_valid_door_tile(self, map):
        # Get all wall tiles as a list
        wall_tiles = map.get_all_tiles_of_value(88)
        
        # Valid door tiles needs a floor on one side and a blank spot on the
        # other side.
        # We will choose a wall tile at random and see if this is valid
        # We will go until the list is exhausted
        while(len(wall_tiles) > 0):
            random_wall_index = random.randint(0, len(wall_tiles) - 1)
            wall = wall_tiles[random_wall_index]

            # First find where the floor tile is
            floor = (-1, -1)
            target = (-1, -1)
            if map.get_tile(wall[0] - 1, wall[1]) == 46:
                floor = (wall[0] - 1, wall[1])
                target = (wall[0] + 1, wall[1])
            elif map.get_tile(wall[0] + 1, wall[1]) == 46:
                floor = (wall[0] + 1, wall[1])
                target = (wall[0] - 1, wall[1])
            elif map.get_tile(wall[0], wall[1] - 1) == 46:
                floor = (wall[0], wall[1] - 1)
                target = (wall[0], wall[1] + 1)
            elif map.get_tile(wall[0], wall[1] + 1) == 46:
                floor = (wall[0], wall[1] + 1)
                target = (wall[0], wall[1] - 1)
            else:
                # Reached a corner piece
                wall_tiles.remove(wall)
                continue

            # Check the opposite tile
            if map.get_tile(target[0], target[1]) != 0:
                wall_tiles.remove(wall)
                continue

            # Check if a 3x3 room can even be built here
            if map.is_perimeter_tile(target[0], target[1]):
                wall_tiles.remove(wall)
                continue

            # If we made it here, this is a valid door tile!
            return {
                "door": wall,
                "target": target
            }
        return None
    
    def place_door(self, map, x, y):
        map.set_tile(x, y, 68)
        return map

    def _should_be_wall_tile(self, corner_x, corner_y, size_x, size_y, cur_x, cur_y):
        if cur_x != corner_x and cur_y != corner_y and \
            cur_x != corner_x + size_x - 1 and cur_y != corner_y + size_y - 1:
            return 0
        return 1
