import toml
from road import Road
from vehicle import Vehicle
from route import Route

class Scenario:

    vehicles_0 = None
    vehicle_spawns = None


    def __init__(self, path=None):
        self.set_default_config()

        if path:
            config = toml.load(path)
    
            for attr, val in config.items():
                setattr(self, attr, val)

    def set_default_config(self):
        roads = ([
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
        ])

        map = []
        for (start, stop) in roads:
            map.append(Road(start, stop))
        self.map = map

        self.starting_vehicles = []
        self.starting_vehicles.append(Vehicle(Route([map[4], map[3], map[2]])))
        self.starting_vehicles.append(Vehicle(Route([map[4], map[1], map[6]])))
        self.starting_vehicles.append(Vehicle(Route([map[7], map[6], map[5]])))
        self.starting_vehicles.append(Vehicle(Route([map[8], map[9], map[0]])))
        self.starting_vehicles.append(Vehicle(Route([map[0]])))
        self.starting_vehicles.append(Vehicle(Route([map[1]])))
        self.starting_vehicles.append(Vehicle(Route([map[6]])))
        self.starting_vehicles.append(Vehicle(Route([map[7]])))


    def get_updates(self, t_old, t_new):
        pass