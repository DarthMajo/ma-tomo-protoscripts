# This is where the whole map is generated.

import random

import map
import room_generator

class MapGenerator():
    def __init__(self, map_size_x=64, map_size_y=64, fill=85):
        self.map_size_x = map_size_x
        self.map_size_y = map_size_y
        self.fill = fill
        self.max_attempts = 10000
        self.map = map.Map(self.map_size_x, self.map_size_y)
        self.rg = room_generator.RoomGenerator()
        self.verify_settings()

    def calc_filled(self):
        total_area = self.map.get_area()
        used_tiles = 0
        for x in range(self.map.sizeX):
            for y in range(self.map.sizeY):
                if self.map.get_tile(x, y) != 0:
                    used_tiles += 1
        return (used_tiles / total_area) * 100.0

    def generate(self, seed):
        # Generate a map via a seed
        random.seed(seed)

        # Place initial room
        self.place_initial_room()

        # Choose where the next room goes
        attempts = 0
        while self.calc_filled() < self.fill and attempts < self.max_attempts:
            next_room = self.rg.choose_valid_door_tile(self.map)
            self.rg.build_room_smart(self.map, next_room)
            attempts += 1

    def place_initial_room(self):
        room_size_x = random.randint(self.rg.min_room_size, self.rg.max_room_size)
        room_size_y = random.randint(self.rg.min_room_size, self.rg.max_room_size)
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

    def verify_settings(self):
        """Check to see if the settings for world creation are valid"""
        # The room sizes cannot exeed the map size
        if self.rg.max_room_size > self.map_size_x:
            raise ValueError("The maximum room size exeeds the map_x size!")
        if self.rg.max_room_size > self.map_size_y:
            raise ValueError("The maximum room size exceeds the map_y size!")
