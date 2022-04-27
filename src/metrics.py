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
        self.times = []
        self.mean_positions = []
        self.time_pos = []

    def measure(self, t, manager):
        # I tilfelle destruktive operasjoner gjøres så burde denne funksjonen holdes read-only
        #velocities = [car.v for car in manager.vehicles]
        #avg_speed_i = np.average(velocities) if velocities else None
        #med_speed_i = np.median(velocities) if velocities else None
        #self.avg_speeds.append([t, avg_speed_i])
        #self.vel_list.append(avg_speed_i)
        # idle_time = 0
        # for velocity in velocities:
        #     if velocity <= 0.5:
        #         idle_time += 1
        # self.idle_list.append(idle_time)
        #self.deleted_num = manager.deleted_vehicles
        #self.through_light_num = manager.through_light
        #self.lifetime_list = manager.lifetimes
        #self.spawn_times = [car.spawn_time for car in manager.vehicles]
        self.times.append(t)
        self.mean_positions.append(np.mean([car.get_traversed_dist() for car in manager.vehicles]))
        #print(manager.vehicles[0].x)
        
    def finalize(self, duration, manager):
        #self.avg_of_avgs = np.nanmean(np.array([spd if spd else np.nan for spd in np.array(self.avg_speeds)[:,1]]))
        #self.median_of_medians = np.nanmedian(np.array([spd if spd else np.nan for spd in np.array(self.avg_speeds)[:,1]]))
        # mean_speed_list = []
        # for vehicle in manager.vehicles:
        #     traversed = 0
        #     for i in range(vehicle.route.cur_index):
        #         traversed += vehicle.route.roads[i].length
        #     mean_speed_list.append((traversed + vehicle.x)/duration)
        #self.metric_dict['velocities'] = np.array(self.avg_of_avgs) 
        #self.metric_dict['mean_vel'] = np.mean(manager.mean_vel + mean_speed_list)
        # mean_speed_list = []
        # for vehicle in manager.vehicles:
        #     vehicle.traversed_dist += vehicle.x
        #     mean_speed_list.append(vehicle.traversed_dist / (duration-vehicle.spawn_time))
        #print(manager.mean_vel)
        self.metric_dict['mean_vel'] = np.mean(manager.mean_vel)# + mean_speed_list)
        #self.metric_dict['median_vel'] = np.array(self.median_of_medians)
        #self.metric_dict['idle_time'] = np.array(self.idle_list).sum()
        
        #self.deleted_list.append(self.deleted_num)
        self.metric_dict['deleted'] =  manager.deleted_vehicles#np.array(self.deleted_list)

        #self.through_light_list.append(self.through_light_num)
        self.metric_dict['through_light_abs'] = manager.through_light
        self.metric_dict['through_light_rel'] = manager.through_light/manager.cars_spawned#np.array(self.through_light_list)
        #self.liftetimes = manager.lifetimes
        self.spawn_times = [car.spawn_time for car in manager.vehicles]
        self.metric_dict['lifetimes'] = np.mean(manager.lifetimes)
                                                #+ [duration-spawn_time for spawn_time in self.spawn_times])
        self.time_pos = [self.times, self.mean_positions]
        

    def plot_all(self):
        avgs = np.array(self.avg_speeds)
        avg_over_avgs = np.average(avgs[avgs[:,1] != np.array(None)][:,1])
        print(f"Average speed: {avg_over_avgs}")    
        #plotting.plot_timeseries(avgs, "Average speed", "[m/s]")
