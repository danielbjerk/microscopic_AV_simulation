from scenario import Scenario
from simulation import *

# Create simulation
scenario_path = "scenarios/example.toml"
scenario = Scenario()#scenario_path)

sim = Simulation(scenario)

# Start simulation
sim.run(10000)