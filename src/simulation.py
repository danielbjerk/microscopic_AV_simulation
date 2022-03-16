from traffic_manager import TrafficManager
from trafficlib import *
from vehicle import Vehicle
from route import Route
from road import Road
from random import random, randint
from metrics import Metrics

# from .vehicle_generator import VehicleGenerator
# from .traffic_signal import TrafficSignal

class Simulation:    
    def __init__(self, scenario, config={}):
        self.scenario = scenario
        # Set default configuration
        self.set_default_config()
        self.traffic_manager = TrafficManager(starting_vehicles=scenario.starting_vehicles, map=scenario.map)
        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.t_0 = 0.0            # Time keeping
        self.t = 0.0
        self.animate = True
        self.frame_count = 0    # Frame count keeping
        self.dt = 1/60          # Simulation time step
        self.generate_prob = 0.002 # Probaility of new car on a road
        self.traffic_signals = []



    # def create_gen(self, config={}):
    #     gen = VehicleGenerator(self, config)
    #     self.generators.append(gen)
    #     return gen

    # def create_signal(self, roads, config={}):
    #     roads = [[self.roads[i] for i in road_group] for road_group in roads]
    #     sig = TrafficSignal(roads, config)
    #     self.traffic_signals.append(sig)
    #     return sig
    


    def handle_scenario_updates(scenario_updates):
        # Parse each update, must be handled individually dep. message, update states accordingly.
        pass

    def update(self):
        t_old = self.t
        self.t += self.dt
        t_new = self.t
        self.frame_count += 1

        # Implementer senere
        #scenario_updates = self.scenario.get_updates(t_old, t_new)
        #scenario_results = self.handle_scenario_updates(scenario_updates)   # Gjerne update-meldinger
        
        self.traffic_manager.update_traffic(self.dt)

        for start_road in self.scenario.routes:
            self.generate_vehicle(self.scenario.routes[start_road])

        # for signal in self.traffic_signals:
        #     signal.update(self)

    def generate_vehicle(self, routes):
        # Easy fix for now. 
        if random() < self.generate_prob:
            route = routes[randint(0, len(routes)-1)]
            route = Route([self.scenario.map[r] for r in route])
            smart_vehicle_adoption = 0.9    # TODO: variabel
            if random() < smart_vehicle_adoption:
                self.traffic_manager.add_vehicle(Vehicle(route, {"smart": True}))
            else:
                self.traffic_manager.add_vehicle(Vehicle(route, {"smart": False}))

    def run(self, steps):
        if self.animate: win = window.init_animation()

        metrics = Metrics() # Burde kanskje være klassevariabel i simulation? Kanskje ikke?

        for _ in range(steps):  # Eller, while not stop
            self.update()

            metrics.measure(self.t, self.traffic_manager.vehicles)

            if self.animate: win.animation_step((self.traffic_manager.vehicles_on_road, self.t, self.frame_count))

        return metrics
