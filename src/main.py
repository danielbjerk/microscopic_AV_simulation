from scenario import Scenario
from simulation import *
import toml

# Create simulation
scenario_path = "scenarios/example.toml"
scenario_config = toml.load(scenario_path)
scenario = Scenario(scenario_config)

sim = Simulation(scenario, {"animate": True})

# Start simulation
fps = 60
dur = 20
metrics = sim.run(fps*dur)

# Post-processing/plotting/storing of important results
metrics.plot_all()
