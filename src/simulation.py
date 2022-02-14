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
    
    def __init__(self, scenario, dict_sim_config) -> None:
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
