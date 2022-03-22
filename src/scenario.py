from road import Road

class Scenario:
    def __init__(self, config=None):
        if not config: config = self.default_config()
        
        map = []
        for (start, stop) in config["roads"]:
            map.append(Road(start, stop))
        self.map = map

        # TODO: Refactor. Jeg bruker bare indekser for veier i stedet for Roads. Er det dumt? Vi har jo map.
        # routes er en dictionary fra source til liste med ruter. Rutene er også bare en liste med vei-indekser.
        self.sources = list(set([r[0] for r in config["legal_routes"]]))
        self.routes = {s: [r for r in config["legal_routes"] if r[0]==s] for s in self.sources}        

        # Dictionary: {source: rate}. Source is int and rate is float.
        self.arrival_times = {source: time for source, time in zip(self.sources, config["arrival_times"])}

        self.starting_vehicles = []

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