from scenario import Scenario
from simulation import *
import toml
import random
import numpy

random.seed(0)
numpy.random.seed(0)

# Create simulation
scenario_path = "scenarios/straight_with_lights.toml"
scenario_config = toml.load(scenario_path)
scenario = Scenario(scenario_config)

sim = Simulation(scenario, animate = True)

# Start simulation

metrics = sim.run(20)


# Post-processing/plotting/storing of important results
metrics.plot_all()
