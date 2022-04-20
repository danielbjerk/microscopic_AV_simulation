from scenario import Scenario
from simulation import *
import toml

# Create simulation
scenario_path = "scenarios/cross_with_lights.toml"
scenario_config = toml.load(scenario_path)
scenario = Scenario(scenario_config)

sim = Simulation(scenario, animate = True)

# Start simulation

metrics = sim.run(80)


# Post-processing/plotting/storing of important results
metrics.plot_all()
