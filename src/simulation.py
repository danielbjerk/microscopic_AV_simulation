from traffic_manager import TrafficManager
from trafficlib import *
from vehicle import DumbVehicle, SmartVehicle
from route import Route
from random import random, randint, seed
from metrics import Metrics
from numpy.random import default_rng
import scenario as scen

def run_N_simulations(scenario_config, N, dur_secs, **config):
    metrics = []
    for i in range(N):
        scenario_i = scen.Scenario(scenario_config)
        print(f"Running simulation {i+1}...")
        sim = Simulation(scenario_i, **config)
        metric_i = sim.run(dur_secs)
        metrics.append(metric_i)
    return metrics

class Simulation:    
    def __init__(self, scenario, **config):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)
        
        self.scenario = scenario
        self.traffic_manager = TrafficManager(sources=scenario.sources, starting_vehicles=scenario.starting_vehicles, map=scenario.map, lights=scenario.lights)
        
        self.generator = default_rng(54321)
        seed(0)

        self.sources = scenario.sources
        self.ex_arrival_times = scenario.arrival_times # Expected arrival times
        self.arrival_times = {source: self.generator.exponential(time) for source, time in self.ex_arrival_times.items()}

    def set_default_config(self):
        self.t = 0.0            # Time keeping
        self.frame_count = 0    # Frame count keeping
        self.fps = 60           # Frames per second
        self.dt = 1/self.fps    # Simulation time step
        self.traffic_signals = []
        self.smart_vehicle_adoption = 0.5

    # def create_signal(self, roads, config={}):
    #     roads = [[self.roads[i] for i in road_group] for road_group in roads]
    #     sig = TrafficSignal(roads, config)
    #     self.traffic_signals.append(sig)
    #     return sig
    


    def handle_scenario_updates(scenario_updates):
        # Parse each update, must be handled individually dep. message, update states accordingly.
        pass

    def update(self):
        # t_old = self.t
        self.t += self.dt
        # t_new = self.t
        self.frame_count += 1

        # Implementer senere
        #scenario_updates = self.scenario.get_updates(t_old, t_new)
        #scenario_results = self.handle_scenario_updates(scenario_updates)   # Gjerne update-meldinger
        
        self.traffic_manager.update_traffic(self.dt, self.t)

        for source in self.sources:
            self.generate_vehicle(source, self.scenario.routes[source])

        # for signal in self.traffic_signals:
        #     signal.update(self)

    def generate_vehicle(self, source, routes):
        if self.t >= self.arrival_times[source]:
            # Generate new vehicle at source
            random_route = routes[randint(0, len(routes)-1)]
            route = Route([self.scenario.map[r] for r in random_route])

            # Add a smart car or a normal car to the queue.
            if random() < self.smart_vehicle_adoption:
                self.traffic_manager.add_vehicle(source, SmartVehicle(route))
            else:
                vehicle = DumbVehicle(route)
                # Stocastic reaction time
                vehicle.T = max(0, vehicle.T + self.generator.normal(0, 0.0695))
                self.traffic_manager.add_vehicle(source, vehicle)

            # Draw arrival time for the next vehicle at this source
            self.arrival_times[source] = self.t + self.generator.exponential(self.ex_arrival_times[source])

    def run(self, duration, steps_per_frame = 1):
        """Run the simulation. The duration is in seconds."""
        if self.animate:
            win = Window()
            win.start_animation()

        metrics = Metrics() # Burde kanskje være klassevariabel i simulation? Kanskje ikke?

        for _ in range(duration*self.fps):
            for _ in range(steps_per_frame):
                self.update()
                metrics.measure(self.t, self.traffic_manager.vehicles)

            if self.animate:
                quit = win.animation_step(
                    (self.traffic_manager.vehicles_on_road,
                    self.traffic_manager.lights,
                    self.t,
                    self.frame_count))
            
                if quit:
                    break

        metrics.finalize()

        return metrics
