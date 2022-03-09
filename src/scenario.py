from road import Road
from vehicle import Vehicle
from route import Route

class Scenario:

    vehicles_0 = None
    vehicle_spawns = None


    def __init__(self, config=None):
        if not config: config = self.default_config()
        
        map = []
        for (start, stop) in config["roads"]:
            map.append(Road(start, stop))
        self.map = map

        # TODO: Refactor. Jeg bruker bare indekser for veier i stedet for Roads. Er det dumt? Vi har jo map.
        # routes er en dictionary fra start_road til liste med ruter. Rutene er også bare en liste med vei-indekser.
        start_roads = set([r[0] for r in config["legal_routes"]])
        self.routes = {s: [r for r in config["legal_routes"] if r[0]==s] for s in start_roads}        

        self.starting_vehicles = []

        # for attr, val in config.items():
        #     setattr(self, attr, val)

    def default_config(self):
        config = {}
        config["roads"] = [
            ((300, 98), (0, 98)),
            ((0, 102), (300, 102)),
            ((180, 60), (0, 60)),
            ((220, 55), (180, 60)),
            ((300, 30), (220, 55)),
            ((180, 60), (160, 98)),
            ((158, 130), (300, 130)),
            ((0, 178), (300, 178)),
            ((300, 182), (0, 182)),
            ((160, 102), (155, 180))
        ]

        config["legal_routes"] = [[4, 3, 2], 
        [4, 1, 6], 
        [7, 6, 5], 
        [8, 9, 0],
        [2, 9, 8]
        ]

        return config

    def get_updates(self, t_old, t_new):
        pass