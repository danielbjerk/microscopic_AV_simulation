from vehicle import *
from simulation import *

# Create simulation
sim = Simulation()

# Add multiple roads
sim.create_roads([
    ((300, 98), (0, 98)),
    ((0, 102), (300, 102)),
    ((180, 60), (0, 60)),
    ((220, 55), (180, 60)),
    ((300, 30), (220, 55)),
    ((180, 60), (160, 98)),
    ((158, 130), (300, 130)),
    ((0, 178), (300, 178)),
    ((300, 182), (0, 182)),
    ((160, 102), (155, 180))
])

sim.roads[4].vehicles.append(
  Vehicle({
    "path": [4, 3, 2]
  })
)

sim.roads[0].vehicles.append(Vehicle())
sim.roads[1].vehicles.append(Vehicle())
sim.roads[6].vehicles.append(Vehicle())
sim.roads[7].vehicles.append(Vehicle())

# Start simulation
sim.run(1)