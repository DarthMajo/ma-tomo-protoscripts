# The prototype for a town

class Map():
    def __init__(self, x, y):
        self.map = self.init_map(x, y)
        self.sizeX = x
        self.sizeY = y

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
                line += str(self.map[y][x]) + ' '
            print(line)
