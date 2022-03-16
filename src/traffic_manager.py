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

    def vehicle_in_front(self, vehicle):    # trenger ikke være klasse-metode
        """
        Notes:
        Warning! Will not take account for vehicles a single super-small road-segment ahead.
        """
        cur_road = vehicle.route.cur_road
        all_vehicles = self.vehicles_on_road[cur_road]
        cur_index = all_vehicles.index(vehicle)
        
        if not cur_index:
            in_front =  None
        else:
            in_front = all_vehicles[cur_index - 1]
        return in_front

    def add_vehicle(self, vehicle):
        if vehicle in self.vehicles:
            raise Exception("Undefined behaviour, vehicle already in simulation")
        else:
            self.vehicles.append(vehicle)
            self.vehicles_on_road[vehicle.route.cur_road].append(vehicle)
            return ("vehicle_added", vehicle)

    def remove_vehicle(self, vehicle):
        try:
            self.vehicles.remove(vehicle)
            self.vehicles_on_road[vehicle.route.cur_road].remove(vehicle)
            return ("vehicle_removed", vehicle)
        except IndexError:
            print("Vehicle somehow already removed?")
            return ("vehicle_already_removed", vehicle)

    def iterate_route(self, vehicle):
        old_road = vehicle.route.cur_road
        new_road = vehicle.route.iterate()
        if not new_road:
            return self.remove_vehicle(vehicle)
        else:
            self.vehicles_on_road[old_road].remove(vehicle)
            self.vehicles_on_road[new_road].append(vehicle)
            vehicle.x = 0
            return ("vehicle_iterated_route", vehicle)

    def parse_vehicle_update_msg(self, update_msg):        
        if not update_msg: return
        msg_type, msg_sender = update_msg
        if msg_type == "traversed_road":
            result = self.iterate_route(msg_sender)
        elif msg_type == "other_update_type":
            # do something else
            pass
        return result

    def update_traffic(self, dt):
        
        vehicle_results = [v.update(dt, self.vehicle_in_front(v)) for v in self.vehicles]   # TODO: None-lead car hardcoded
        results = [self.parse_vehicle_update_msg(msg) for msg in vehicle_results]

        # Do more? What other traffic parts must be updated at each time moment?
        
        # Change traffic lights here? Then both vehicles and TrafficManager contains references to road
        # Fix by changing vehicles reference to road to a list of road-names, while 
        # trafficmanager stores the actual map (container of entire road object (name, signals) + relationships to other roads)
        
        return results
