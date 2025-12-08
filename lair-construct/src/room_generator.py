# This will create the individual room in a map

import random

class RoomGenerator():
    def __init__(self, min_room_size=3, max_room_size=10):
        self.max_room_size = max_room_size
        self.min_room_size = min_room_size
        self.verify_settings()

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
    
    def build_room_smart(self, m, location):
        """Builds a room based on parsing its surroundings"""
        # Find from the door the depth the room can be
        dx = location['door'][0]
        dy = location['door'][1]
        tx = location['target'][0]
        ty = location['target'][1]
        direction = self._find_depth_direction(location['door'], location['target'])
        max_depth = self._calc_depth(m, location['door'], direction)

        # Calculate initial room sizes
        room_size_x_limit = self.max_room_size if (direction == 'north' or direction == 'south') else max_depth
        room_size_y_limit = self.max_room_size if (direction == 'east' or direction == 'west') else max_depth
        if room_size_x_limit <= self.min_room_size:
            return 0
        if room_size_y_limit <= self.min_room_size:
            return 0
        room_size_x = random.randint(self.min_room_size, room_size_x_limit)
        room_size_y = random.randint(self.min_room_size, room_size_y_limit)

        # Now here is the tricky part. We know how far we can go one direction, but not the other
        # We will try with the rooms initial size
        # If that that does not work, we will randomly displace the room until all options are gone
        # If we are out of options, reduce the size of the room in non-depth direction
        original_entrances = list(range(1, room_size_x - 1)) if (direction == 'north' or direction == 'south') else list(range(1, room_size_y - 1))
        entrances = original_entrances.copy()
        room_layout_not_chosen = True
        while room_layout_not_chosen and len(entrances) > 0:
            # Choose a random entrance
            entrance = entrances[random.randint(0, len(entrances)-1)]

            # Calculate the initial corner
            pos_x = -1
            pos_y = -1

            if direction == 'south':
                pos_x = tx - entrance
                pos_y = dy
            elif direction == 'north':
                pos_x = tx - entrance
                pos_y = dy - (room_size_y - 1)
            elif direction == 'east':
                pos_x = dx
                pos_y = ty - entrance
            else:
                pos_x = dx - (room_size_x - 1)
                pos_y = ty - entrance

            # See if this room works
            if self._is_empty_plot(m, pos_x, pos_y, room_size_x, room_size_y):
                room_layout_not_chosen = False
                for x in range(pos_x, pos_x + room_size_x):
                    for y in range(pos_y, pos_y + room_size_y):
                        if self._should_be_wall_tile(pos_x, pos_y, room_size_x, room_size_y, x, y):
                            m.set_tile(x, y, 88)
                        else:
                            m.set_tile(x, y, 46)

                # Finally, plop the door
                m = self.place_door(m, location['door'][0], location['door'][1])
            
            # If this entrance failed, remove and try again
            entrances.remove(entrance)

            # If we made it here, all possible locations for this room size failed
            if len(entrances) <= 0:
                if direction == 'north' or direction == 'south':
                    room_size_x -= 1
                else:
                    room_size_y -= 1
                
                if room_size_x < self.min_room_size:
                    break
                if room_size_y < self.min_room_size:
                    break

                original_entrances = list(range(1, room_size_x - 1)) if (direction == 'north' or direction == 'south') else list(range(1, room_size_y - 1))
                entrances = original_entrances.copy()

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
    
    def set_max_size(self, x):
        self.max_room_size = x
        self.verify_settings()
    
    def set_min_size(self, x):
        self.min_room_size = x
        self.verify_settings()
    
    def verify_settings(self):
        if self.min_room_size > self.max_room_size:
            raise ValueError("The minimum room size cannot be greater than the maximum room size!")
        if self.min_room_size <= 2:
            raise ValueError("The minimum room size cannot be less than 3!")
        if self.max_room_size <= 2:
            raise ValueError("The maximum room size cannot be less than 3!")
    
    def _calc_depth(self, map, door, direction):
        dx = door[0]
        dy = door[1]

        # Count how many empty tiles until we reach a tile marked
        for i in range(1, self.max_room_size):
            displacer = (0, 0)
            if direction == "north":
                displacer = (0, -i)
            elif direction == "south":
                displacer = (0, i)
            elif direction == "east":
                displacer = (i, 0)
            else:
                displacer = (-i, 0)
            if map.get_tile(dx + displacer[0], dy + displacer[1]) != 0:
                return i + 1
            
        return self.max_room_size
    
    def _find_depth_direction(self, door, target):
        x_diff = door[0] - target[0]
        y_diff = door[1] - target[1]
        if x_diff > 0:
            return "west"
        elif x_diff < 0:
            return "east"
        elif y_diff < 0:
            return "south"
        elif y_diff > 0:
            return "north"
        else:
            raise ValueError("Door and target cannot be in the same location!")
        
    def _is_empty_plot(self, map, pos_x, pos_y, size_x, size_y):
        if not map.is_tile_in_bounds(pos_x, pos_y) or \
            not map.is_tile_in_bounds(pos_x + size_x, pos_y + size_y):
            return False

        # We do not care for the perimeter blocks.
        for x in range(pos_x + 1, pos_x + size_x - 1):
            for y in range(pos_y + 1, pos_y + size_y - 1):
                if map.get_tile(x, y) != 0:
                    return False
        return True

    def _should_be_wall_tile(self, corner_x, corner_y, size_x, size_y, cur_x, cur_y):
        if cur_x != corner_x and cur_y != corner_y and \
            cur_x != corner_x + size_x - 1 and cur_y != corner_y + size_y - 1:
            return 0
        return 1
