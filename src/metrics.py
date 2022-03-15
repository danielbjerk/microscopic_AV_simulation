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

    def plot_all(self):
        avgs = np.array(self.avg_speeds)
        plotting.plot_timeseries(avgs, "Average speed", "[m/s]")
