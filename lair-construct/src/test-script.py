import map_generator

mg = map_generator.MapGenerator(80, 24)
mg.generate(42)
mg.map.print_map()
