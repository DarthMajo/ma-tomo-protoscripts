# The prototype for building road patterns

import random

import map

class RoadGenerator():
    def __init__(self, map):
        self.map = map
    
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
                return (random.randint(1, x - 2), 0) # North
            else:
                return (random.randint(1, x - 2), y - 1) # South
        else:
            # East or West
            if random.randint(0, 1) == 0:
                return (0, random.randint(1, y - 2)) # West
            else:
                return (x - 1, random.randint(1, y - 2)) # East
            
    def generate(self):
        gt = rg._choose_gate_tile(map_size_x, map_size_y)
        self.map.set_tile(gt[0], gt[1], 'G')
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
