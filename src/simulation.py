from trafficlib import *
from road import Road
from copy import deepcopy
# from .vehicle_generator import VehicleGenerator
# from .traffic_signal import TrafficSignal

class Simulation:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.t = 0.0            # Time keeping
        self.frame_count = 0    # Frame count keeping
        self.dt = 1/60          # Simulation time step
        self.roads = []         # Array to store roads
        # self.generators = []
        self.traffic_signals = []

    def create_road(self, start, end):
        road = Road(start, end)
        self.roads.append(road)
        return road

    def create_roads(self, road_list):
        for road in road_list:
            self.create_road(*road)

    # def create_gen(self, config={}):
    #     gen = VehicleGenerator(self, config)
    #     self.generators.append(gen)
    #     return gen

    # def create_signal(self, roads, config={}):
    #     roads = [[self.roads[i] for i in road_group] for road_group in roads]
    #     sig = TrafficSignal(roads, config)
    #     self.traffic_signals.append(sig)
    #     return sig

    def update(self):
        # Update every road
        for road in self.roads:
            road.update(self.dt)

        # Add vehicles
        # for gen in self.generators:
        #     gen.update()

        # for signal in self.traffic_signals:
        #     signal.update(self)

        # Check roads for out of bounds vehicle
        for road in self.roads:
            # If road has no vehicles, continue
            if len(road.vehicles) == 0: continue
            # If not
            vehicle = road.vehicles[0]
            # If first vehicle is out of road bounds
            if vehicle.x >= road.length:
                # If vehicle has a next road
                if vehicle.current_road_index + 1 < len(vehicle.path):
                    # Update current road to next road
                    vehicle.current_road_index += 1
                    # Create a copy and reset some vehicle properties
                    new_vehicle = deepcopy(vehicle)
                    new_vehicle.x = 0
                    # Add it to the next road
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    self.roads[next_road_index].vehicles.append(new_vehicle)
                # In all cases, remove it from its road
                road.vehicles.popleft() 
        # Increment time
        self.t += self.dt
        self.frame_count += 1


    def run(self, steps):
        win = Window(self)
        win.zoom = 5

        def loop(sim):
            for _ in range(steps):
                self.update()

        win.loop(loop)

'''
class Simulation:

    # Class variables

    scenario = None

    t_0 = None
    t_1 = None
    t = None
    h = None
    N = None

    vehicles = None


    # Class methods
    
    def __init__(self, scenario, dict_sim_config=None) -> None:
        if not dict_sim_config:
            dict_sim_config = self.default_config()
        
        self.scenario = scenario
        
        self.t_0 = dict_sim_config["time_start"]
        self.t = self.t_0
        self.t_1 = dict_sim_config["time_end"]
        self.h = dict_sim_config["time_step"]
        self.N = (self.t_1 - self.t_0)/self.h

        self.vehicles = scenario.initial_vehicles

    def handle_scenario_updates(scenario_updates):
        # Parse each update, must be handled individually dep. message, update states accordingly.
        pass

    def update(self):
        t_old = self.t
        self.t += self.h
        t_new = self.t

        scenario_updates = self.scenario.get_updates(t_old, t_new)
        self.handle_scenario_updates(scenario_updates)   # Gjerne update-meldinger
        
        self.vehicles.update(t_new) # hvem eier vehicles?
'''