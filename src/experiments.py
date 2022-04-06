import test_multiple_adoption_rates
import pandas as pd


def plot_from_excel(filename):
    dF = pd.read_excel(filename)
    metrics = ['velocities', 'idle_time', 'deleted', 'through_light']
    #metrics = ['deleted']
    for metric in metrics:
        print(metric)
        test_multiple_adoption_rates.boxplot_from_dF(dF, metric)

plot_from_excel('metrics.xlsx')

