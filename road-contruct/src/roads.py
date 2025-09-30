# The prototype for building road patterns

import random

import map

class RoadGenerator():
    def __init__(self, map):
        self.map = map
        self.gate_direction = None
        self.gate_location = None
        self.initial_road_location = None
    
    def _choose_gate_tile(self, x, y):
        # Do we do the north, south, east, or west corner?
        #   0 = N
        #   1 = S
        #   2 = E
        #   3 = W
        edge = random.randint(0, 3)

        if edge < 2:
            # North or South
            if random.randint(0, 1) == 0:
                self.gate_direction = 0
                return (random.randint(1, x - 2), 0) # North
            else:
                self.gate_direction = 1
                return (random.randint(1, x - 2), y - 1) # South
        else:
            # East or West
            if random.randint(0, 1) == 0:
                self.gate_direction = 3
                return (0, random.randint(1, y - 2)) # West
            else:
                self.gate_direction = 2
                return (x - 1, random.randint(1, y - 2)) # East
    
    def _choose_initial_road_tile(self):
        match self.gate_direction:
            case 0:
                return (self.gate_location[0], self.gate_location[1] + 1)
            case 1:
                return (self.gate_location[0], self.gate_location[1] - 1)
            case 2:
                return (self.gate_location[0] - 1, self.gate_location[1])
            case 3:
                return (self.gate_location[0] + 1, self.gate_location[1])
            
    def _is_valid_tile(self, x, y):
        # First check if the tile is within the map
        if not self.map.is_tile_in_bounds(x, y):
            return False
        
        # Check to see if something else is already built there
        if self.map.get_tile(x, y) != 0:
            return False

        # Check if we are creating a road that will create a 2x2 intersection
        if self._will_create_two_by_two(x, y):
            return False
        
        return True
    
    def _will_create_two_by_two(self, x, y):
        return self._check_corner_for_three_roads(x, y, 'nw') or \
        self._check_corner_for_three_roads(x, y, 'ne') or \
        self._check_corner_for_three_roads(x, y, 'sw') or \
        self._check_corner_for_three_roads(x, y, 'se')
    
    def _check_corner_for_three_roads(self, x, y, direction):
        road_count = 0
        neighbor_x = x
        neighbor_y = y
        
        match direction:
            case 'nw':
                neighbor_x -= 1
                neighbor_y -= 1
            case 'ne':
                neighbor_x += 1
                neighbor_y -= 1
            case 'sw':
                neighbor_x -= 1
                neighbor_y += 1
            case 'se':
                neighbor_x += 1
                neighbor_y += 1
        
        # Check if neighbors are in bounds
        if self.map.is_tile_in_bounds(neighbor_x, y) and \
        self.map.is_tile_in_bounds(x, neighbor_y) and \
        self.map.is_tile_in_bounds(neighbor_x, neighbor_y):
            # We are in bounds, so let's count how many roads are there
            if self.map.get_tile(neighbor_x, y) == ord('r'):
                road_count += 1
            if self.map.get_tile(x, neighbor_y) == ord('r'):
                road_count += 1
            if self.map.get_tile(neighbor_x, neighbor_y) == ord('r'):
                road_count += 1

            # If there are three roads, this is an invalid placement
            if road_count >= 3:
                return True
        
        # If we made it here it is a valid road placement
        return False
            
    def generate(self):
        self.gate_location = self._choose_gate_tile(map_size_x, map_size_y)
        self.initial_road_location = self._choose_initial_road_tile()

        self.map.generate_walls()
        self.map.set_tile(self.gate_location[0], self.gate_location[1], ord('G'))
        self.map.set_tile(self.initial_road_location[0], self.initial_road_location[1], ord('r'))
        self.map.generate_grass()

        return self.map

if __name__ == '__main__':
    map_size_x = 16
    map_size_y = 9
    myMap = map.Map(map_size_x, map_size_y)

    # Let's start the road stuff
    rg = RoadGenerator(myMap)

    # Get the map with updated roads
    myMap = rg.generate()
    myMap.print_map()
