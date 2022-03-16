from random import random
import numpy as np

def idm(s_desired, delta_s, v, a_max, v_max, delta):
        a_freeroad = a_max*(1-(v/v_max)**delta) 
        a_interaction = -a_max*(s_desired/delta_s)**2
        a = a_freeroad + a_interaction
        return a



class Vehicle:
    def __init__(self, route):        
        self.route = route

        self.l = 4              # length of vehicle i
        self.v_max = 16.6       # max desired speed of vehicle i. Set this as road.v_limit?
        self.x = 0
        self.v = self.v_max
        self.a = 0

    def control_acceleration(self, car_infront):
        pass

    def update_physics(self, dt):
        if self.v + self.a*dt < 0:
            self.x -= (1/2)*(self.v**2)/self.a
            self.v = 0
        else:
            self.v += self.a*dt
            self.x += self.v*dt + self.a*(dt**2)/2

    def change_color(self):
        pass
    
    def update(self, dt, car_infront=None):
        self.control_acceleration(car_infront)
        
        self.update_physics(dt)
        
        self.change_color()

        # Common for all 
        if self.x >= self.route.cur_road.length:
            return ("traversed_road", self)



class DumbVehicle(Vehicle):
    def __init__(self, route, config={}):
        super().__init__(route)

        #Parameters for idm: 
        self.T = 2              # Reaction time of vehicle i's driver. Set to 0 when self.smart==True.
        self.delta = 4          # smoothness of the acceleration
        self.s0 = 4             # min desired distance between vehicle i and i-1 

        self.a_max = 1.44       # Max accel of vehicle i    # 4s
        self.b_max = 4.61       # comfortable deceleration of vehicle i

        self.stopped = False

        self.smart = False

        self.v_max = 7  # tmp

        self.color = (0, 0, 255)

        for key, attr in config.items():
            setattr(self, key, attr)

    def control_acceleration(self, car_infront):
        if car_infront:
            delta_s = car_infront.x-self.x-car_infront.l
            delta_v = self.v-car_infront.v 
            s_desired = self.s0+self.v*self.T+self.v*(delta_v)/(2*np.sqrt(self.a_max*self.b_max))
            self.a = idm(s_desired, delta_s, self.v, self.a_max, self.v_max, self.delta)
        else:
            self.a = self.a_max*(1-(self.v/self.v_max)**self.delta) 



class SmartVehicle(Vehicle):
    def __init__(self, route, config={}):
        super().__init__(route)

        #Parameters for idm: 
        self.T = 2             # Reaction time of vehicle i's driver. Set to 0 when self.smart==True.
        self.delta = 4          # smoothness of the acceleration
        self.s0 = 4             # min desired distance between vehicle i and i-1 
        self.link_window = 4

        self.a_max = 1.44       # Max accel of vehicle i    # 4s
        self.b_max = 4.61       # comfortable deceleration of vehicle i

        self.stopped = False

        self.smart = True
        self.state = "init"

        self.color = (255, 0, 0)

        for key, attr in config.items():
            setattr(self, key, attr)

    def control_acceleration(self, car_infront):
        # Change state, may be moved to own state-machine function
        if car_infront:
            delta_s = car_infront.x - self.x - car_infront.l
            delta_v = self.v - car_infront.v
            if car_infront.smart:
                s_desired = self.s0 + self.link_window
            else:
                s_desired = self.s0 + self.v*self.T + self.v*(delta_v)/(2*np.sqrt(self.a_max*self.b_max))

            if -0.2*self.link_window < delta_s - s_desired < 1.2*self.link_window and car_infront.smart:
                self.state = "linked"
            elif delta_s <= self.s0:
                self.state = "too_close_infront"
            else:
                self.state = "far_from_infront"

        elif not car_infront:
            self.state = "alone_on_road"
        
        else:
            self.state = "undefined"
        

        # Take action based on state
        if self.state == "alone_on_road":
            new_a = self.a_max*(1-(self.v/self.v_max)**self.delta)     # Freeroad-acceleration

        elif self.state == "too_close_infront" or \
        self.state == "far_from_infront":
            new_a = idm(s_desired, delta_s, self.v, self.a_max, self.v_max, self.delta)

        elif self.state == "linked":
            # Hacky løsning
            # Trenger egen tilstand "linking" som bruker idm frem til hastigheter er innenfor terskel 
            K_p = -self.b_max/2
            new_a = car_infront.a + K_p*delta_v

        else:
            new_a = self.a
        
        self.a = new_a
        return

    def change_color(self):
        if self.state == "linked":
            self.color = (120, 120, 120)
        elif self.state == "too_close_infront" or \
        self.state == "far_from_infront" or \
        self.state == "alone_on_road":
            self.color = (155, 0, 155)
        else:
            self.color = (255, 255, 255)
