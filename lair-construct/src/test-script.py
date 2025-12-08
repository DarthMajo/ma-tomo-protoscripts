import map_generator

x_size = int(input("What is the map size x:"))
y_size = int(input("What is the map size y:"))
seed = int(input("Enter a seed:"))

mg = map_generator.MapGenerator(x_size, y_size)
mg.generate(seed)
mg.map.print_map()
