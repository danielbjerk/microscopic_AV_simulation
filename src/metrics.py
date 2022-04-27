import numpy as np


class Metrics:
    def __init__(self):
        self.avg_speeds = []

        self.metric_dict = {}
        self.vel_list = []
        self.idle_list = []
        self.cars_list = []
        self.deleted_list = []
        self.through_light_list = []
        self.times = []
        self.mean_positions = []
        self.time_pos = []

    def measure(self, t, manager):
        self.times.append(t)
        self.mean_positions.append(
            np.mean([car.get_traversed_dist() for car in manager.vehicles]))

    def finalize(self, duration, manager):
        self.metric_dict['mean_vel'] = np.mean(
            manager.mean_vel)
        self.metric_dict['deleted'] = manager.deleted_vehicles
        # self.through_light_list.append(self.through_light_num)
        self.metric_dict['through_light_abs'] = manager.through_light
        self.metric_dict['through_light_rel'] = manager.through_light / \
            manager.cars_spawned  # np.array(self.through_light_list)
        #self.liftetimes = manager.lifetimes
        self.spawn_times = [car.spawn_time for car in manager.vehicles]
        self.metric_dict['lifetimes'] = np.mean(manager.lifetimes)
        # + [duration-spawn_time for spawn_time in self.spawn_times])
        self.time_pos = [self.times, self.mean_positions]

    def plot_all(self):
        avgs = np.array(self.avg_speeds)
        avg_over_avgs = np.average(avgs[avgs[:, 1] != np.array(None)][:, 1])
        print(f"Average speed: {avg_over_avgs}")
