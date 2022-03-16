from scenario import Scenario
from simulation import *
import toml
import random

random.seed(0)

# Create simulation
scenario_path = "scenarios/straight.toml"
scenario_config = toml.load(scenario_path)
scenario = Scenario(scenario_config)

sim = Simulation(scenario, {"animate": True})

# Start simulation
fps = 60
dur = 1000
metrics = sim.run(fps*dur)

# Post-processing/plotting/storing of important results
metrics.plot_all()
