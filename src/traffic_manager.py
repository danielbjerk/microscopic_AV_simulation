from turtle import update
from vehicle import Vehicle

class TrafficManager:

    def __init__(self, starting_vehicles, map) -> None:
        self.vehicles = starting_vehicles# List(Vehicle)# biler som skal følge ruten som inneholder veier.
        self.vehicles_on_road = dict() # Dictionary mellom road og hvilke vehicles som er på den veien. (unødvendig?)
        
        for road in map:
            self.vehicles_on_road[road] = []
        for v in starting_vehicles:
            self.vehicles_on_road[v.route.cur_road].append(v)

    def all_vehicles_on_road(self, road):
        return self.vehicles_on_road[road]

    def add_vehicle(self, vehicle):
        if vehicle in self.vehicles:
            raise Exception("Undefined behaviour, vehicle already in simulation")
        else:
            self.vehicles.append(vehicle)
            self.vehicles_on_road[vehicle.route.cur_road].append(vehicle)
            return ("vehicle_added", vehicle.id)

    def remove_vehicle(self, vehicle):
        try:
            self.vehicles.remove(vehicle)
            self.vehicles_on_road[vehicle.route.cur_road].remove(vehicle)
            return ("vehicle_removed", vehicle.id)
        except IndexError:
            print("Vehicle somehow already removed?")
            return ("vehicle_already_removed", vehicle.id)

    def iterate_route(self, vehicle):
        old_road = vehicle.route.cur_road
        new_road = vehicle.route.iterate()
        if not new_road:
            return self.remove_vehicle(vehicle)
        else:
            self.vehicles_on_road[old_road].remove(vehicle)
            self.vehicles_on_road[new_road].append(vehicle)
            return ("vehicle_iterated_route", vehicle.id)

    def parse_vehicle_update_msg(self, update_msg):        
        msg_type, msg_sender = update_msg
        if msg_type == "traversed_road":
            result = self.iterate_route(msg_sender)
        elif msg_type == "other_update_type":
            # do something else
            pass
        return result

    def update_traffic(self, dt):
        vehicle_results = [v.update(dt) for v in self.vehicles]
        results = [self.parse_vehicle_update_msg(msg) for msg in vehicle_results]

        # Do more? What other traffic parts must be updated at each time moment?
        
        # Change traffic lights here? Then both vehicles and TrafficManager contains references to road
        # Fix by changing vehicles reference to road to a list of road-names, while 
        # trafficmanager stores the actual map (container of entire road object (name, signals) + relationships to other roads)
        return results
