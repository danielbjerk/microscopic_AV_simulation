from vehicle import Vehicle
from simulation import Simulation

from road import Road
from simulation import Simulation

class TrafficLight:
    light = {0:'Red', 1:'Green'}

    def __init__(self, road):
        self.road = road
        self.pos = road.end 
        self.cycle_index = 0
        #self.cycles_dict = {1:(True,False) , 2:((True,False),(False,True))} ## Er dette felles for alle trafikklys
        self.cycle = (True, False)#self.cycles_dict[len(road)]
        self.time_at_last_change = 0
        self.time_in_cur_cycle = 0
        self.maxtime = 10
        self.stop_zone = 40

    def green(self):
        return self.cycle[self.cycle_index]

    def update(self, t):
        self.time_in_cur_cycle = t - self.time_at_last_change
        if self.time_in_cur_cycle >= self.maxtime:
            self.cycle_index += 1
            self.cycle_index %= len(self.cycle)
            self.time_in_cur_cycle = 0
            self.time_at_last_change = t
        return self.cycle[self.cycle_index]
