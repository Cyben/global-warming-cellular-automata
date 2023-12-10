from Simulation import Simulation
from World import World

print("Configuring World...")
world: World = World(map_file="world.dat")

print("Configuring Simulation...")
simulation = Simulation(world=world)
simulation.mainloop()
