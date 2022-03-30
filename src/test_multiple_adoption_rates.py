from scenario import Scenario
import simulation
import toml

from time import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create simulation
scenario_path = "scenarios/straight_with_lights.toml"
scenario_config = toml.load(scenario_path)
#scenario = Scenario(scenario_config)
dF  = pd.DataFrame()
adopt_rates = np.linspace(0, 1, 51)
meta_metrics = []

tic = time()
# Skal bli dataframe
metric_dict = {}
for rate in adopt_rates:
    print(f"---------Running simulation for {rate} smart vehicle adoption rate---------")

    N = 100
    #metrics = simulation.run_N_simulations(scenario, N=100, dur_secs=20, sim_config={"animate" : True})  # dupliserte biler beholdes på tvers av sims
    metrics = simulation.run_N_simulations(scenario_config, N=N, dur_secs=60, 
                                            animate=False, smart_vehicle_adoption=rate)

    its = np.array(range(N))
    avgs = np.array([m.avg_of_avgs for m in metrics])
    meta_metrics.append(np.nanmean(avgs))
    
    for m in metrics:
        for key in m.metric_dict:
            new_key = str(rate) + ' ' + key
            
            if new_key in metric_dict.keys():
                val_list = metric_dict[new_key]
            else: 
                val_list = []
            val_list += [m.metric_dict[key]]
            metric_dict[new_key] = val_list
dF = pd.DataFrame(metric_dict)
toc = time()
dF.to_excel('metrics.xlsx')


# meta_metrics = np.array(meta_metrics)
# plt.plot(adopt_rates, meta_metrics)
# plt.show()
print(f'time = {toc-tic} s')

def plot_from_dF(dF, value, error = False, plot_sdt = False):
    rates = []
    avg = []
    std = []
    for key in dF:
        key_split = key.split(' ')
        if key_split[1] == value:
            rates.append(float(key_split[0]))
            avg.append(dF[key].mean())
            std.append(dF[key].std())
    plt.plot(rates, avg, 'o-')
    if error:
        plt.errorbar(rates, avg, std, color = 'tab:gray')
    
    plt.xlabel('adoption rate of autonomus vehicle')
    plt.ylabel(value)
    plt.show()
    if plot_sdt:
        plt.plot(rates, std)
        plt.xlabel('adoption rate of autonomus vehicle')
        plt.ylabel(f'SD {value}')
        plt.show()

plot_from_dF(dF, 'velocities', True, True)
plot_from_dF(dF, 'idle_time', True, True)
plot_from_dF(dF, 'deleted', True)
plot_from_dF(dF, 'through_light', True)