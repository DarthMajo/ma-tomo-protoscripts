# This will create the individual room in a map

class RoomGenerator():
    def __init__(self):
        pass

    def build_room(self, x, y, m, door_x, door_y)
        # Builds a room of x and y size on map m
        # The door location is where the origin of the room will begin
        
        # First, calc direction the room will be placed. This will be done by
        # checking the adjacent floor tile. The room will begin on the tile
        # opposite from the floor tile and the door.

        # See if we can put room size x and y in the room.
        #     If we cannot, see if x or y that is the problem. Scale down and try again.
        #     If the room size becomes x=3,y=3 and still invalid, abort.
        pass

    def calculate_room_starting_tile(self, m, door_x, door_y):
        pass

    def is_room_placement_valid(self):
        pass
