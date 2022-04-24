import simulation
import toml

from time import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create simulation
scenario_path = "scenarios/straight_with_lights.toml"
scenario_config = toml.load(scenario_path)
'''
dF  = pd.DataFrame()
meta_metrics = []
metric_dict = {}    # Skal bli dataframe
'''
# Hyper-parameters

adopt_rates = np.round(np.linspace(0, 1, 50+1), decimals=2)
num_sims_pr_scen = 80
dur_single_sim_secs = 500

def run_Simulations(adopt_rates, num_sims_pr_scen, dur_single_sim_secs, write = False):
    dF  = pd.DataFrame()
    meta_metrics = []
    metric_dict = {}    # Skal bli dataframe
    pos_time_rate_dict = {}
    tic = time()
    for rate in adopt_rates:
        tic_1 = time()
        print(f"---------Running simulation for {rate} smart vehicle adoption rate---------")
        print(f"---------Running simulation for {dur_single_sim_secs} total_time---------")

        sim_metrics = simulation.run_N_simulations(scenario_config, N=num_sims_pr_scen, dur_secs=dur_single_sim_secs, 
                                                config={"animate" : False, "smart_vehicle_adoption" : rate})
        '''
        its = np.array(range(num_sims_pr_scen))
        avgs = np.array([m.avg_of_avgs for m in sim_metrics])
        meta_metrics.append(np.nanmean(avgs))
        '''
        for m in sim_metrics:
            m.time_pos.append([rate for i in range(len(m.time_pos[0]))])
            pos_time_rate_dict[rate] = m.time_pos
            for key in m.metric_dict:
                new_key = str(rate) + ' ' + key
                if new_key in metric_dict.keys():
                    val_list = metric_dict[new_key]
                else: 
                    val_list = []
                val_list += [m.metric_dict[key]]
                metric_dict[new_key] = val_list
        toc_1 = time()
        print(f'time = {toc_1-tic_1} s')
    dF = pd.DataFrame(metric_dict)
    dF_pos_time_rate = pd.DataFrame(pos_time_rate_dict)
    toc = time()
    if write:
        dF.to_excel('metrics.xlsx')
        dF_pos_time_rate.to_excel('pos_time_rate.xlsx')

    print(f'time = {toc-tic} s')
    return dF, dF_pos_time_rate


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
    title_dict = {'velocities': r'Fart av biler', 
                    'idle_time' : 'Total stillestående tid', 
                    'deleted': 'Biler som når enden', 
                    'through_light': 'Gjennomflyt av biler i lyskryss',
                    'lifetimes': 'Tid brukt på vei'}

    y_label_dict = {'velocities': r'Gjennomsnittsfart $[\frac{km}{h}]$', 
                    'idle_time' : 'Samlet ventetid [s]', 
                    'deleted': 'Biler fjernet fra simulering', 
                    'through_light': 'Biler gjennom lys',
                    'lifetimes': 'Tid [s]'}
    scaling = 1
    if value == 'velocities' or value == 'mean_vel': 
        scaling =  3.6 ## m/s to km/h
    elif value == 'idle_time':
        scaling = 1 / 60 ## frames to seconds
    rates = []
    avgs = []
    for key in dF:
        key_split = key.split(' ')
        if key_split[1] == value:
            
            rates.append(float(key_split[0]))
            avgs.append(np.array(dF[key].tolist()) * scaling)
    #plt.plot(rates, avg, 'o-')
    #print(np.unique(rates)[::4])
    print(avgs)
    print(np.mean(avgs))
    print(len(rates), len(avgs))
    plt.boxplot(avgs, positions= rates, widths=0.01)
    plt.xlim((min(rates)-0.05, max(rates)+0.05))
    if value in title_dict:
        plt.title(title_dict[value])
        plt.ylabel(y_label_dict[value])
    else:
        plt.ylabel(value)
    plt.xlabel('Andel autonome kjøretøy')
    plt.xticks(ticks=np.unique(rates)[::10], labels=np.unique(rates)[::10])
    
    plt.savefig('out/' + value + '_pb.pdf')
    plt.show()
    
def time_plot(dF_pos_time_rate, plot_rates = None, filename = None):
    pos_list = []
    times_list = []
    rates_list = []
    #print('dF_pos_time_rate', dF_pos_time_rate.keys())
    #print(dF_pos_time_rate[0.0].to_list())
    if plot_rates:
        fig, axs = plt.subplots(len(plot_rates),1)
        for rate in plot_rates:
            pos, times, rates = dF_pos_time_rate[rate].to_list()
            #print(pos)
            pos_list.append(pos)
            times_list.append(times)
            rates_list.append(rates)
        print(axs[0])
        for i in range(len(plot_rates)):
            axs[i].plot(times_list[i], pos_list[i], '-')
            axs[i].set_title(f'Rate {plot_rates[i]}')
            axs[i].set_xlabel('Time [s]')
            axs[i].set_ylabel('Mean Position [m]')
        plt.tight_layout()
        if filename:
            plt.savefig(filename)
        plt.show()
    


dF, dF_pos_time_rate = run_Simulations(adopt_rates, num_sims_pr_scen, dur_single_sim_secs, write = True)
#print(dF.keys())
#print(dF_time.keys())
#dF_pos_time_rate.to_excel('pos_time_rate.xlsx')
#boxplot_from_dF(dF, 'velocities')
#boxplot_from_dF(dF, 'mean_vel')
#time_plot(dF_pos_time_rate, [0.0, 0.5, 1.0], )
#boxplot_from_dF(dF, 'idle_time')
#boxplot_from_dF(dF, 'lifetimes')
#boxplot_from_dF(dF, 'median_vel')

#boxplot_from_dF(dF, 'velocities')
#boxplot_from_dF(dF, 'idle_time')
#boxplot_from_dF(dF, 'mean_vel')
#boxplot_from_dF(dF, 'lifetimes')
#boxplot_from_dF(dF, 'deleted')
#boxplot_from_dF(dF, 'through_light')
