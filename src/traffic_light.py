class TrafficLight:
    def __init__(self, road, is_init_green=True):
        self.road = road
        self.pos = road.end
        self.time_at_last_change = 0
        self.is_green = is_init_green
        self.green_time = 30
        self.red_time = 30
        self.stop_zone = 40
        self.show = True

    def update(self, t):
        if self.is_green and t - self.time_at_last_change >= self.green_time:
            self.is_green = False
            self.time_at_last_change = t
        if not self.is_green and t - self.time_at_last_change >= self.red_time:
            self.is_green = True
            self.time_at_last_change = t
        return self.is_green
