# The prototype for building road patterns

import map

if __name__ == '__main__':
    myMap = map.Map(10, 5)
    myMap.set_tile(4, 4, 1)
    print(myMap.get_tile(4,4))
    myMap.print_map()
