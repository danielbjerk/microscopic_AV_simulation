from scenario import Scenario
from simulation import *
import toml

# Create simulation
scenario_path = "scenarios/straight_queue_from_nowhere.toml"
scenario_config = toml.load(scenario_path)
scenario = Scenario(scenario_config)
scenario.lights[0].show = False
scenario.lights[0].green_time = 60
scenario.lights[0].red_time = 10

sim = Simulation(scenario, animate=True, smart_vehicle_adoption=0.0)

# Start simulation

metrics = sim.run(130, 4)


# Post-processing/plotting/storing of important results
metrics.plot_all()
