import matplotlib.pyplot as plt

def plot_timeseries(ts, title, ylab):
    fig, ax = plt.subplots()
    ax.plot(ts[:,0], ts[:,1])
    ax.set_title(title)
    ax.set_ylabel(ylab)
    ax.set_xlabel("Time [s]")
    plt.show()
