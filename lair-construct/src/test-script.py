import map_generator

mg = map_generator.MapGenerator(25, 25)
mg.generate(42)
mg.map.print_map()
