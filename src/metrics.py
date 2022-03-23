import numpy as np
import plotting


class Metrics:
    def __init__(self) -> None:
        self.avg_speeds = []

    def measure(self, t, vehicles):
        # I tilfelle destruktive operasjoner gjøres så burde denne funksjonen holdes read-only
        velocities = [car.v for car in vehicles]
        avg_speed_i = np.average(velocities) if velocities else None
        self.avg_speeds.append([t, avg_speed_i])

    def finalize(self):
        self.avg_of_avgs = np.nanmean(np.array([spd if spd else np.nan for spd in np.array(self.avg_speeds)[:,1]]))

    def plot_all(self):
        avgs = np.array(self.avg_speeds)
        avg_over_avgs = np.average(avgs[avgs[:,1] != np.array(None)][:,1])
        print(f"Average speed: {avg_over_avgs}")
        #plotting.plot_timeseries(avgs, "Average speed", "[m/s]")
