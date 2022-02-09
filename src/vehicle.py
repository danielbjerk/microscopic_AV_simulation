class Vehicle:

    def __init__(self, vehicle_config) -> None:
        self.passengers = 0
        self.pos_percentage = 0
        self.speed = 0

        self.at_target = False

        self.route = calculate_route()

    def update(self):
        msg = receive() # -> meldinger om andre biler(s) posisjon og fart

        delta = make_decision(msg)

        feedback = perform_action(delta)

        self.pos_percentage += h*delta
        self.speed += h*delta



