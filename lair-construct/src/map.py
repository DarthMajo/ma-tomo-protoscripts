# The prototype for a town

class Map():
    def __init__(self, x, y):
        self.map = self.init_map(x, y)
        self.sizeX = x
        self.sizeY = y

    def get_all_tiles_of_value(self, val):
        all_val_tiles = []
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                if self.get_tile(x, y) == val:
                    all_val_tiles.append((x, y))
        return all_val_tiles

    def get_area(self):
        return self.sizeX * self.sizeY
    
    def get_area_usable(self):
        return (self.sizeX - 1) * (self.sizeY - 1)

    def get_tile(self, x, y):
        if not self.is_tile_in_bounds(x,y):
            return -1

        return self.map[y][x]
    
    def is_perimeter_tile(self, x, y):
        if x == 0 or x == self.sizeX - 1 or \
            y == 0 or y == self.sizeY - 1:
            return True
        return False
    
    def is_tile_in_bounds(self, x, y):
        if x < 0 or x >= self.sizeX:
            return False
        if y < 0 or y >= self.sizeY:
            return False
        return True

    def init_map(self, x, y):
        mapY = []

        for _ in range(y):
            mapX = []
            for _ in range(x):
                mapX.append(0)
            mapY.append(mapX)

        return mapY
    
    def print_map(self):
        for y in range(self.sizeY):
            line = ""
            for x in range(self.sizeX):
                if self.map[y][x] == 0:
                    line += '~'
                else:
                    line += str(chr(self.map[y][x]))
            print(line)

    def set_tile(self, x, y, new_value):
        self.map[y][x] = new_value
