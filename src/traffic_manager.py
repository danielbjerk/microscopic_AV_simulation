class TrafficManager:

    def __init__(self, sources, starting_vehicles, map, lights):
        # biler som skal følge ruten som inneholder veier.
        self.vehicles = starting_vehicles
        # Dictionary mellom road og hvilke vehicles som er på den veien. (unødvendig?)
        self.vehicles_on_road = {road: [] for road in map}

        # En del av quick fixen "source_road" i update_traffic. Må fikses opp i. Kanksje er det en bedre løsning å ha mappet?
        self.map = map

        self.lights = lights
        lights_on_road = {road: None for road in map}
        for l in lights:
            lights_on_road[l.road] = l
        self.lights_on_road = lights_on_road

        # Vehicles are buffered before spawning
        self.vehicle_buffers = {source: [] for source in sources}

        # Number of vehicles removed.
        self.deleted_vehicles = 0
        # Number of vehicles through a light
        self.through_light = 0
        # List of total lifetime of deleted cars
        self.lifetimes = []
        self.mean_vel = []
        self.cars_spawned = len(starting_vehicles)

        for v in starting_vehicles:
            self.vehicles_on_road[v.route.cur_road].append(v)

    def all_vehicles_on_road(self, road):
        return self.vehicles_on_road[road]

    def vehicle_in_front(self, vehicle):
        cur_road = vehicle.route.cur_road
        all_vehicles = self.vehicles_on_road[cur_road]
        cur_index = all_vehicles.index(vehicle)

        if not cur_index:
            # TODO: Better implementation of "in front"-logic
            next_road = vehicle.route.next_on_route()
            if next_road:
                if self.vehicles_on_road[next_road]:
                    in_front = self.vehicles_on_road[next_road][-1]
                else:
                    in_front = None
            else:
                in_front = None
        else:
            in_front = all_vehicles[cur_index - 1]
        return in_front

    def add_vehicle(self, source, vehicle):
        # Keep a maximum of one vehicle in the buffer.
        if not self.vehicle_buffers[source]:
            self.vehicle_buffers[source].append(vehicle)

    def remove_vehicle(self, vehicle, t):
        try:
            vehicle.x = 0
            self.deleted_vehicles += 1
            self.lifetimes.append(t - vehicle.spawn_time)
            self.mean_vel.append(vehicle.full_dist/self.lifetimes[-1])

            self.vehicles.remove(vehicle)
            self.vehicles_on_road[vehicle.route.cur_road].remove(vehicle)
            return ("vehicle_removed", vehicle)
        except IndexError:
            print("Vehicle somehow already removed?")
            return ("vehicle_already_removed", vehicle)

    def iterate_route(self, vehicle, t):
        old_road = vehicle.route.cur_road
        new_road = vehicle.route.iterate()
        # Adds distance of old road when traversed
        vehicle.traversed_dist += old_road.length
        if not new_road:
            return self.remove_vehicle(vehicle, t)
        else:
            self.vehicles_on_road[old_road].remove(vehicle)
            self.vehicles_on_road[new_road].append(vehicle)
            vehicle.x = 0
            if self.lights_on_road[old_road]:
                self.through_light += 1
            return ("vehicle_iterated_route", vehicle)

    def parse_vehicle_update_msg(self, update_msg, t):
        if not update_msg:
            return
        msg_type, msg_sender = update_msg
        if msg_type == "traversed_road":
            result = self.iterate_route(msg_sender, t)
        elif msg_type == "other_update_type":
            # do something else
            pass
        return result

    def update_traffic(self, dt, t):
        for source, buffer in self.vehicle_buffers.items():
            if buffer:
                vehicle = buffer[0]
                source_road = self.map[source]
                if not self.vehicles_on_road[source_road]\
                        or self.vehicles_on_road[source_road][-1].x > vehicle.s0 + vehicle.l:
                    if self.vehicles_on_road[source_road] and self.vehicles_on_road[source_road][-1].x < 5*vehicle.s0:
                        vehicle.v = self.vehicles_on_road[source_road][-1].v
                    self.vehicles.append(vehicle)
                    self.vehicles_on_road[source_road].append(vehicle)
                    buffer.pop()
                    self.cars_spawned += 1

        light_statuses = [l.update(t) for l in self.lights]
        vehicle_results = [v.update(dt, self.vehicle_in_front(
            v), self.lights_on_road[v.route.cur_road]) for v in self.vehicles]
        results = [self.parse_vehicle_update_msg(
            msg, t) for msg in vehicle_results]

        return results
