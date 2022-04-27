from scenario import Scenario
from simulation import *
import toml

# Create simulation
scenario_path = "scenarios/straight_with_lights.toml"
scenario_config = toml.load(scenario_path)
scenario = Scenario(scenario_config)

sim = Simulation(scenario, animate=True, smart_vehicle_adoption=0.0)

# TODO: Seed the generator so the spawning is the same for the two simulations
metrics1 = sim.run(40, 5)

scenario = Scenario(scenario_config)
sim = Simulation(scenario, animate=True, smart_vehicle_adoption=1.0)

metrics2 = sim.run(40, 5)

# Post-processing/plotting/storing of important results
metrics1.plot_all()
metrics2.plot_all()
