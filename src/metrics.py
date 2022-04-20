import numpy as np
import plotting


class Metrics:
    def __init__(self):
        self.avg_speeds = []

        self.metric_dict = {}
        self.vel_list = []
        self.idle_list = []
        self.cars_list = []
        self.deleted_list = []
        self.through_light_list = []

    def measure(self, t, manager):
        # I tilfelle destruktive operasjoner gjøres så burde denne funksjonen holdes read-only
        velocities = [car.v for car in manager.vehicles]
        avg_speed_i = np.average(velocities) if velocities else None
        #med_speed_i = np.median(velocities) if velocities else None
        self.avg_speeds.append([t, avg_speed_i])
        self.vel_list.append(avg_speed_i)
        idle_time = 0
        for velocity in velocities:
            if velocity <= 0.5:
                idle_time += 1
        self.idle_list.append(idle_time)
        self.deleted_num = manager.deleted_vehicles
        self.through_light_num = manager.through_light
        self.lifetime_list = manager.lifetimes
        self.spawn_times = [car.spawn_time for car in manager.vehicles]
        
    def finalize(self, duration):
        self.avg_of_avgs = np.nanmean(np.array([spd if spd else np.nan for spd in np.array(self.avg_speeds)[:,1]]))
        self.median_of_medians = np.nanmedian(np.array([spd if spd else np.nan for spd in np.array(self.avg_speeds)[:,1]]))
        self.metric_dict['velocities'] = np.array(self.avg_of_avgs)
        #self.metric_dict['median_vel'] = np.array(self.median_of_medians)
        self.metric_dict['idle_time'] = np.array(self.idle_list).sum()
        
        #self.deleted_list.append(self.deleted_num)
        self.metric_dict['deleted'] =  self.deleted_num#np.array(self.deleted_list)

        #self.through_light_list.append(self.through_light_num)
        self.metric_dict['through_light'] = self.through_light_num#np.array(self.through_light_list)
        #self.liftetimes = manager.lifetimes
        
        self.metric_dict['lifetimes'] = np.mean(self.lifetime_list 
                                                + [duration-spawn_time for spawn_time in self.spawn_times])
        
    def plot_all(self):
        avgs = np.array(self.avg_speeds)
        avg_over_avgs = np.average(avgs[avgs[:,1] != np.array(None)][:,1])
        print(f"Average speed: {avg_over_avgs}")    
        #plotting.plot_timeseries(avgs, "Average speed", "[m/s]")
