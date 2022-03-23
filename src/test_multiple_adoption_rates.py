from scenario import Scenario
import simulation
import toml

import numpy as np
import matplotlib.pyplot as plt

# Create simulation
scenario_path = "scenarios/example.toml"
scenario_config = toml.load(scenario_path)
#scenario = Scenario(scenario_config)

adopt_rates = np.linspace(0, 1, 51)
meta_metrics = []
for rate in adopt_rates:
    print(f"---------Running simulation for {rate} smart vehicle adoption rate---------")

    N = 40
    #metrics = simulation.run_N_simulations(scenario, N=100, dur_secs=20, sim_config={"animate" : True})  # dupliserte biler beholdes på tvers av sims
    metrics = simulation.run_N_simulations(scenario_config, N=N, dur_secs=60, 
                                            animate=False, smart_vehicle_adoption=rate)

    its = np.array(range(N))
    avgs = np.array([m.avg_of_avgs for m in metrics])
    meta_metrics.append(np.nanmean(avgs))
    #plt.plot(its, avgs)
    #plt.show()

meta_metrics = np.array(meta_metrics)
plt.plot(adopt_rates, meta_metrics)
plt.xlabel("Smart vehicle adoption rate [%]")
plt.ylabel("Average speed [m/s]")
plt.show()
