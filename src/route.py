from road import Road

class Route:

    def __init__(self, list_roads) -> None:
        self.roads = list_roads
        self.cur_index = 0
        self.cur_road = self.roads[self.cur_index]


    def iterate(self) -> Road:
        self.cur_index += 1
        if self.cur_index >= len(self.roads):
            return None
        else:
            self.cur_road = self.roads[self.cur_index]
            return self.cur_road

    def next_on_route(self) -> Road:
        if self.cur_index + 1 >= len(self.roads):
            return None
        else:
            return self.roads[self.cur_index + 1]