from scenario import Scenario
from simulation import *
import toml

# Create simulation
scenario_path = "scenarios/example.toml"
scenario_config = toml.load(scenario_path)
scenario = Scenario(scenario_config)

sim = Simulation(scenario)

# Start simulation
sim.run(10000)