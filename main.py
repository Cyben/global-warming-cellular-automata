from Simulation import Simulation
from World import World

print("Configuring World...")
world: World = World(map_file="world.dat",
                     pollution_heat_factor=0.7,
                     rain_temperature_factor=0.4,
                     city_pollution=0.01,
                     land_initial_temperature=17,
                     sea_initial_temperature=10,
                     iceberg_initial_temperature=-17,
                     forest_initial_temperature=15,
                     city_initial_temperature=22)

print("Configuring Simulation...")
simulation = Simulation(world=world, last_gen=365)
simulation.mainloop()
