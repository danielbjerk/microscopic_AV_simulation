from numpy.linalg import norm


class Road:
    def __init__(self, start, end):
        self.start = start
        self.end = end

        self.init_properties()

    def init_properties(self):
        self.length = norm([self.end[0] - self.start[0],
                           self.end[1] - self.start[1]])
        self.angle_sin = (self.end[1]-self.start[1]) / self.length
        self.angle_cos = (self.end[0]-self.start[0]) / self.length
        # self.angle = np.arctan2(self.end[1]-self.start[1], self.end[0]-self.start[0])
