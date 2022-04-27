import cProfile
import pstats


import simulation
import toml
import numpy

# Create simulation
scenario_path = "scenarios/straight_with_lights.toml"
scenario_config = toml.load(scenario_path)
num_sims_pr_scen = 3
dur_single_sim_secs = 500
rate = 0.0


def fun(x): return simulation.run_N_simulations(scenario_config, N=num_sims_pr_scen, dur_secs=dur_single_sim_secs,
                                                animate=False, smart_vehicle_adoption=rate)


profile = cProfile.Profile()
profile.runcall(simulation.run_N_simulations, scenario_config, num_sims_pr_scen,
                dur_single_sim_secs, {"animate": False, "smart_vehicle_adoption": 0.0})
# profile.runcall(fun(0))
ps = pstats.Stats(profile)
ps.sort_stats('cumtime')
ps.print_stats()
