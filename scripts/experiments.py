import toml
from time import time
import numpy as np
import test_multiple_adoption_rates
import pandas as pd


def plot_from_excel(filename):
    dF = pd.read_excel(filename)
    metrics_str = ['velocities', 'idle_time', 'deleted', 'through_light']
    #metrics = ['deleted']
    for metric_str in metrics_str:
        print(metric_str)
        test_multiple_adoption_rates.boxplot_from_dF(dF, metric_str)


def simulation_vary_time(write):
    # Create simulation
    scenario_path = "scenarios/straight_with_lights.toml"
    scenario_config = toml.load(scenario_path)

    dF = pd.DataFrame()

    adopt_rates = np.round(np.linspace(0, 1, 21), decimals=2,)
    num_sims_pr_scen = 100
    dur_sim_secs = np.linspace(40, 540, 20, dtype='int')
    for dur_single_sim_secs in dur_sim_secs:
        metric_dF = test_multiple_adoption_rates.run_Simulations(adopt_rates,
                                                                 num_sims_pr_scen,
                                                                 dur_single_sim_secs)
        for key in metric_dF:
            dF[key + '_' + str(dur_single_sim_secs)
               ] = metric_dF[key].to_numpy()
    if write:
        dF.to_excel('metrics_Time.xlsx')
    return dF


if __name__ == "__name__":
    plot_from_excel('metrics.xlsx')
    simulation_vary_time(True)
