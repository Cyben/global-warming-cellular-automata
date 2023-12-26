from Simulation import Simulation
from World import World

print("Configuring World...")
world: World = World(map_file="map.txt",
                     pollution_heat_factor=0.2,
                     rain_temperature_factor=0.4,
                     city_pollution=0.2,
                     land_initial_temperature=17,
                     sea_initial_temperature=10,
                     iceberg_initial_temperature=-20,
                     forest_initial_temperature=13,
                     city_initial_temperature=20)

print("Configuring Simulation...")
simulation = Simulation(world=world, last_gen=365)
simulation.mainloop()
