from scenario import Scenario
from simulation import *
import toml

# Create simulation
scenario_path = "scenarios/straight_with_lights.toml"
scenario_config = toml.load(scenario_path)
scenario = Scenario(scenario_config)

sim = Simulation(scenario, animate=True, smart_vehicle_adoption=1.0)

# Start simulation
metrics = sim.run(200, 5)

# Post-processing/plotting/storing of important results
metrics.plot_all()
