from traffic_manager import TrafficManager
from trafficlib import *
from vehicle import DumbVehicle, SmartVehicle
from route import Route
from metrics import Metrics
from numpy.random import default_rng, uniform, randint
import scenario as scen

from time import time

def run_N_simulations(scenario_config, N, dur_secs, **config):
    N_metrics = []
    for i in range(N):
        scenario_i = scen.Scenario(scenario_config)
        print(f"Running simulation {i+1}...")
        tic_1 = time()
        sim = Simulation(scenario_i, **config)
        metric_i = sim.run(dur_secs,5)
        N_metrics.append(metric_i)
        toc_1 = time()
        print(f'time = {toc_1-tic_1} s')
    return N_metrics

class Simulation:    
    def __init__(self, scenario, **config):
        self.t = 0.0            # Time keeping
        self.frame_count = 0    # Frame count keeping
        self.fps = 60           # Frames per second
        self.dt = 1/self.fps    # Simulation time step
        self.traffic_signals = []
        self.smart_vehicle_adoption = 0.5

        for attr, val in config.items():
            setattr(self, attr, val)
        
        self.scenario = scenario
        self.traffic_manager = TrafficManager(sources=scenario.sources, 
                                            starting_vehicles=scenario.starting_vehicles, 
                                            map=scenario.map, 
                                            lights=scenario.lights)
        
        self.generator = default_rng()

        self.sources = scenario.sources
        self.ex_arrival_times = scenario.arrival_times # Expected arrival times
        self.arrival_times = {source: self.generator.exponential(time) for source, time in self.ex_arrival_times.items()}

    def update(self):
        self.t += self.dt
        self.frame_count += 1
        
        self.traffic_manager.update_traffic(self.dt, self.t)

        for source in self.sources:
            self.generate_vehicle(source, self.scenario.routes[source])


    def generate_vehicle(self, source, routes):
        if self.t >= self.arrival_times[source]:
            # Generate new vehicle at source
            random_route = routes[randint(0, len(routes))]
            route = Route([self.scenario.map[r] for r in random_route])

            # Add a smart car or a normal car to the queue.
            if uniform() < self.smart_vehicle_adoption:
                self.traffic_manager.add_vehicle(source, SmartVehicle(route, self.t))
            else:
                vehicle = DumbVehicle(route, self.t)
                # Stocastic reaction time
                vehicle.T = max(0, vehicle.T + self.generator.normal(0, 0.2))
                self.traffic_manager.add_vehicle(source, vehicle)

            # Draw arrival time for the next vehicle at this source
            self.arrival_times[source] = self.t + self.generator.exponential(self.ex_arrival_times[source])

    def run(self, duration, steps_per_frame = 1):
        """Run the simulation. The duration is in seconds."""
        if self.animate:
            win = Window()
            win.start_animation()

        metrics_init = False
        init_metrics_after_secs = 85

        for _ in range(duration*self.fps//steps_per_frame):
            if self.t >= init_metrics_after_secs and not metrics_init:
                metrics = Metrics() # Burde kanskje være klassevariabel i simulation? Kanskje ikke?
                metrics_init = True
            
            for _ in range(steps_per_frame):
                self.update()
                if metrics_init: metrics.measure(self.t, self.traffic_manager)

            if self.animate:
                quit = win.animation_step(
                    (self.traffic_manager.vehicles_on_road,
                    self.traffic_manager.lights,
                    self.t,
                    self.frame_count))
            
                if quit:
                    break

        metrics.finalize(duration, self.traffic_manager)

        return metrics
