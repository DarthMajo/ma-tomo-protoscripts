# The prototype for building road patterns

import random

import map

class RoadGenerator():
    def __init__(self, map, road_coverage=18):
        self.built_tiles = set()
        self.gate_direction = None
        self.gate_location = None
        self.initial_road_location = None
        self.map = map
        self.road_coverage = road_coverage
        self.tail_tile_queue = []
        self.valid_roads = [ord('r'), ord('G'), 9472, 9474, 9484, 9488, 9496, 9492, 9500, 9508, 9516, 9524, 9532]

    def _attempt_build_tile(self, x, y, neighbors, free_space):
        # We choose the intial tile and see what is around
        # If there are two, have a greater chance to plop down,
        # and so on for three and four.
        # If there is only one, have a good chance to go opposite direction;
        # 1/8 of chance to turn
        # After plop, pop node out of list and append all 90 degree null nodes
        built = []

        if len(neighbors) == 1:
            dice_roll = random.randint(0, 999)

            # We want a decent chance the road goes straight
            # Here are the odds:
            #   67.5% the road is straight
            #   22.5% the road turns
            #   10% no additional road
            if dice_roll < 675:
                # Find the opposite road tile than what is the current neighbor
                neighbor = neighbors[0]
                diffx = neighbor[0] - x
                diffy = neighbor[1] - y
                desired_tile = (x - diffx, y - diffy)

                # Build this tile if it is an allowed tile
                if desired_tile in free_space:
                    free_space = self._build(desired_tile, free_space)
                else:
                    # If we made it here, we want a road, but it is invalid.
                    # We want to then try to curve the road
                    dice_roll += 225
            if dice_roll >= 675 and dice_roll < 900:
                # Turn a 90 or 270 degree turn
                neighbor = neighbors[0]
                diffx = neighbor[0] - x
                diffy = neighbor[1] - y
                flip_a_coin = random.randint(0,1)
                desired_tile = (-1, -1)
                
                # We have to see what axis the road comes from
                # So whichever diff=0 is what we choose
                if diffy == 0:
                    # Then we flip for East vs. West
                    if flip_a_coin == 0 and (x, y - 1) in free_space:
                        desired_tile = (x, y - 1)
                    else:
                        desired_tile = (x, y + 1)
                else:
                    # Then we flip for North vs. South
                    if flip_a_coin == 0 and (x - 1, y) in free_space:
                        desired_tile = (x - 1, y)
                    else:
                        desired_tile = (x + 1, y)

                # Build the tile
                if desired_tile in free_space:
                    free_space = self._build(desired_tile, free_space)

            #else:
            #    pass # DON'T BUILD

        elif len(neighbors) == 2:
            if len(free_space) >= 1:
                index = random.randint(0, len(free_space) - 1)
                desired_tile = free_space[index]
                free_space = self._build(desired_tile, free_space)
        elif len(neighbors) == 3:
            if len(free_space) >= 1:
                index = random.randint(0, len(free_space) - 1)
                desired_tile = free_space[index]
                free_space = self._build(desired_tile, free_space)
        elif len(neighbors) == 4:
            if len(free_space) >= 1:
                index = random.randint(0, len(free_space) - 1)
                desired_tile = free_space[index]
                free_space = self._build(desired_tile, free_space)

        return built
    
    def _build(self, desired_tile, free_space=None):
        self.map.set_tile(desired_tile[0], desired_tile[1], ord('r'))
        if free_space:
            free_space.remove(desired_tile)
        self.tail_tile_queue.append(desired_tile)
        self.built_tiles.add(desired_tile)
        return free_space
    
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
    
    def _process_queue(self):
        while len(self.tail_tile_queue) > 0:
            tile = self.tail_tile_queue.pop(0)
            self._process_tile(tile[0], tile[1])
    
    def _process_tile(self, current_x, current_y):
        # Find out how many neighbors there are that are roads
        check_neighbors = self._process_neighbors(current_x, current_y)
        neighbors = check_neighbors[0]
        free_space = check_neighbors[1]

        # Depending on neighbors, there is a higher chance of building a road
        new_tiles = self._attempt_build_tile(current_x, current_y, neighbors, free_space)
        self.tail_tile_queue.extend(new_tiles)

        return len(new_tiles)
    
    def _process_neighbor(self, x, y, neighbors, free_space):
        tile_value = self.map.get_tile(x, y)
        if tile_value in self.valid_roads:
            neighbors.append((x,y))
        elif self._is_valid_tile(x, y):
            free_space.append((x,y))

        return (neighbors, free_space)
    
    def _process_neighbors(self, current_x, current_y):
        neighbors = []
        free_space = []
        (neighbors, free_space) = self._process_neighbor(current_x - 1, current_y, neighbors, free_space)
        (neighbors, free_space) = self._process_neighbor(current_x, current_y - 1, neighbors, free_space)
        (neighbors, free_space) = self._process_neighbor(current_x + 1, current_y, neighbors, free_space)
        (neighbors, free_space) = self._process_neighbor(current_x, current_y + 1, neighbors, free_space)
        return (neighbors, free_space)
    
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

        # Initial generation of the city borders and the customs gate
        self.map.generate_walls()
        self.map.set_tile(
            self.gate_location[0],
            self.gate_location[1],
            ord('G')
        )

        # Initial run of the road generation
        self._build((self.initial_road_location[0], self.initial_road_location[1]))
        self._process_queue()

        # Check to see if we need any further roads
        while(self.map.get_tile_population(ord('r')) / self.map.get_area_usable() <= self.road_coverage / 100.0):
            # Choose a random road tile to branch off from
            tile_index = random.randint(0, len(self.built_tiles) - 1)
            tile = list(self.built_tiles)[tile_index]

            # Build on that road tile; should do the process
            self._build((tile[0], tile[1]))
            self._process_queue()

        # Finally, all remaining space is grass
        self.map.generate_grass()

        return self.map
    
    def stylize(self):
        # We will go through every tile in the playable space and check its
        # neighbors for figuring out how to stylize the char... will be
        # important for when we go to Godot
        for y in range(1, self.map.sizeY - 1):
            for x in range(1, self.map.sizeX - 1):
                if self.map.get_tile(x, y) == ord('r'):
                    # Complex ones first
                    if self.map.get_tile(x - 1, y) in self.valid_roads and self.map.get_tile(x + 1, y) in self.valid_roads and self.map.get_tile(x, y - 1) in self.valid_roads and self.map.get_tile(x, y + 1) in self.valid_roads:
                        self.map.set_tile(x, y, 9532)
                    elif self.map.get_tile(x - 1, y) in self.valid_roads and self.map.get_tile(x, y - 1) in self.valid_roads and self.map.get_tile(x + 1, y) in self.valid_roads:
                        self.map.set_tile(x, y, 9524)
                    elif self.map.get_tile(x - 1, y) in self.valid_roads and self.map.get_tile(x, y + 1) in self.valid_roads and self.map.get_tile(x + 1, y) in self.valid_roads:
                        self.map.set_tile(x, y, 9516)
                    elif self.map.get_tile(x + 1, y) in self.valid_roads and self.map.get_tile(x, y + 1) in self.valid_roads and self.map.get_tile(x, y - 1) in self.valid_roads:
                        self.map.set_tile(x, y, 9500)
                    elif self.map.get_tile(x - 1, y) in self.valid_roads and self.map.get_tile(x, y + 1) in self.valid_roads and self.map.get_tile(x, y - 1) in self.valid_roads:
                        self.map.set_tile(x, y, 9508)
                    elif self.map.get_tile(x - 1, y) in self.valid_roads and self.map.get_tile(x, y - 1) in self.valid_roads:
                        self.map.set_tile(x, y, 9496)
                    elif self.map.get_tile(x + 1, y) in self.valid_roads and self.map.get_tile(x, y - 1) in self.valid_roads:
                        self.map.set_tile(x, y, 9492)
                    elif self.map.get_tile(x - 1, y) in self.valid_roads and self.map.get_tile(x, y + 1) in self.valid_roads:
                        self.map.set_tile(x, y, 9488)
                    elif self.map.get_tile(x + 1, y) in self.valid_roads and self.map.get_tile(x, y + 1) in self.valid_roads:
                        self.map.set_tile(x, y, 9484)
                    elif self.map.get_tile(x - 1, y) in self.valid_roads and self.map.get_tile(x + 1, y) in self.valid_roads:
                        self.map.set_tile(x, y, 9472)
                    elif self.map.get_tile(x, y - 1) in self.valid_roads and self.map.get_tile(x, y + 1) in self.valid_roads:
                        self.map.set_tile(x, y, 9474)

if __name__ == '__main__':
    map_size_x = 32
    map_size_y = 32
    myMap = map.Map(map_size_x, map_size_y)

    # Let's start the road stuff
    rg = RoadGenerator(myMap)

    # Get the map with updated roads
    myMap = rg.generate()
    rg.stylize()
    myMap.print_map()
