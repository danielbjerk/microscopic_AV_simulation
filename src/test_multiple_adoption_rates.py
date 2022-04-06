import simulation
import toml

from time import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create simulation
scenario_path = "scenarios/straight_with_lights.toml"
scenario_config = toml.load(scenario_path)

dF  = pd.DataFrame()
meta_metrics = []
metric_dict = {}    # Skal bli dataframe

# Hyper-parameters
adopt_rates = np.round(np.linspace(0, 1, 21), decimals=2)
num_sims_pr_scen = 100
dur_single_sim_secs = 80
def run_Simulations(write = False):
    tic = time()
    for rate in adopt_rates:
        print(f"---------Running simulation for {rate} smart vehicle adoption rate---------")

        metrics = simulation.run_N_simulations(scenario_config, N=num_sims_pr_scen, dur_secs=dur_single_sim_secs, 
                                                animate=False, smart_vehicle_adoption=rate)

        its = np.array(range(num_sims_pr_scen))
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
    if write:
        dF.to_excel('metrics.xlsx')

    print(f'time = {toc-tic} s')
    return dF


# meta_metrics = np.array(meta_metrics)
# plt.plot(adopt_rates, meta_metrics)
# plt.show()


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
        plt.savefig(value + '.pdf')
        plt.show()
'''
plot_from_dF(dF, 'velocities', True, True)
plot_from_dF(dF, 'idle_time', True, True)
plot_from_dF(dF, 'deleted', True)
plot_from_dF(dF, 'through_light', True)
'''
def boxplot_from_dF(dF, value):
    rates = []
    avgs = []
    for key in dF:
        key_split = key.split(' ')
        if key_split[1] == value:
            
            rates.append(float(key_split[0]))
            avgs.append(dF[key].tolist())
    #plt.plot(rates, avg, 'o-')
    #print(np.unique(rates)[::4])
    #print(avgs)
    print(np.mean(avgs))
    plt.boxplot(avgs, positions= rates, widths=0.025)
    plt.xlabel('adoption rate of autonomus vehicle')
    plt.xticks(ticks=np.unique(rates)[::4], labels=np.unique(rates)[::4])
    plt.ylabel(value)
    plt.savefig('out/' + value + '_pb.png')
    plt.show()
    

#boxplot_from_dF(dF, 'velocities', True, True)
'''
boxplot_from_dF(dF, 'velocities')
boxplot_from_dF(dF, 'idle_time')
boxplot_from_dF(dF, 'deleted')
boxplot_from_dF(dF, 'through_light')
'''