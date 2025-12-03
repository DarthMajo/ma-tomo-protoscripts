# This will create the individual room in a map

class RoomGenerator():
    def __init__(self):
        pass

    def build_room(self, pos_x, pos_y, size_x, size_y, m, door_x, door_y):
        # Builds a room of x and y size on map m
        # The door location is where the origin of the room will begin
        for x in range(pos_x, pos_x + size_x):
            for y in range(pos_y, pos_y + size_y):
                # TODO: ADD DOOR FUNCTIONALITY
                if x == door_x and y == door_y:
                    m.set_tile(x, y, 68)
                if self._is_outer_tile(pos_x, pos_y, size_x, size_y, x, y):
                    m.set_tile(x, y, 88)
                else:
                    m.set_tile(x, y, 46)
        return m

    def _is_outer_tile(self, corner_x, corner_y, size_x, size_y, cur_x, cur_y):
        if cur_x != corner_x and cur_y != corner_y and \
            cur_x != corner_x + size_x - 1 and cur_y != corner_y + size_y - 1:
            return 0
        return 1
