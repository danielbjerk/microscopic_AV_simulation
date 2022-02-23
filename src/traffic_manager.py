from vehicle import Vehicle

class TrafficManager:

    def __init__(self, starting_vehicles) -> None:
        vehicles = starting_vehicles# List(Vehicle)# biler som skal følge ruten som inneholder veier.
        vehicles_on_road = dict() # Dictionary mellom road og hvilke vehicles som tilhører den veien. (unødvendig?)
        for v in starting_vehicles:
            vehicles_on_road[v.route.cur_road] = v

    def iterate_route(self, vehicle):
        old_road = vehicle.route.cur_road
        self.vehicles_on_road[old_road].remove(vehicle)
        new_road = vehicle.route.iterate()
        if not new_road:
            # Remove vehicle from simulation here
            raise IndexError("END OF ROAD")
        else:
            self.vehicles_on_road[new_road].append(vehicle)

    def parse_update(self, update_msg):        
        if update_msg.type == "traversed_road":
            self.iterate_route(update_msg.sender)
        elif update_msg.type == "other_update_type":
            # do something else
            pass

    def update_vehicles(self, dt):
        update_msgs = [v.update(dt) for v in self.vehicles]

        for update in update_msgs:
            self.parse_update(update)