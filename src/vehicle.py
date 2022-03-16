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
    def __init__(self, route):
        super().__init__(route)

        #Parameters for idm: 
        self.T = 2              # Reaction time of vehicle i's driver. Set to 0 when self.smart==True.
        self.delta = 4          # smoothness of the acceleration
        self.s0 = 4             # min desired distance between vehicle i and i-1 

        self.a_max = 1.44       # Max accel of vehicle i    # 4s
        self.b_max = 4.61       # comfortable deceleration of vehicle i

        self.stopped = False

        self.smart = False
        self.link = False
        self.copy_next_v = False

        self.color = (0, 0, 255)

    def control_acceleration(self, car_infront):
        if car_infront:
            delta_s = car_infront.x-self.x-car_infront.l
            delta_v = self.v-car_infront.v 
            s_desired = self.s0+self.v*self.T+self.v*(delta_v)/(2*np.sqrt(self.a_max*self.b_max))
            self.a = idm(s_desired, delta_s, self.v, self.a_max, self.v_max, self.delta)
        else:
            self.a = self.a_max*(1-(self.v/self.v_max)**self.delta) 



class SmartVehicle(Vehicle):
    def __init__(self, route):
        super().__init__(route)

        #Parameters for idm: 
        self.T = 0             # Reaction time of vehicle i's driver. Set to 0 when self.smart==True.
        self.delta = 4          # smoothness of the acceleration
        self.s0 = 4             # min desired distance between vehicle i and i-1 

        self.a_max = 1.44       # Max accel of vehicle i    # 4s
        self.b_max = 4.61       # comfortable deceleration of vehicle i

        self.stopped = False

        self.smart = True
        self.link = False
        self.copy_next_v = False

        self.color = (255, 0, 0)

    def control_acceleration(self, car_infront):
        if self.link and car_infront:
            # self.v = car_infront.v    # TODO: Hvordan håndtere at vi ønsker instanteneous endring til self.v = car_infront.v
            # Nå overskriver self.v av physics
            self.a = car_infront.a
        else:
            #update velocity and position
            if self.copy_next_v and car_infront:
                # self.v = car_infront.v    # TODO: Her også!
                self.copy_next_v = False
            
            #update acceleration:
            if car_infront==None:
                self.a = self.a_max*(1-(self.v/self.v_max)**self.delta) #a_freeroad
            elif self.smart and car_infront.smart: 
                delta_s = car_infront.x-self.x-car_infront.l
                delta_v = self.v-car_infront.v 
                s_desired = self.s0 #s_desired can be this small because we copy the car infront
                
                if delta_s-s_desired > 0.2:
                    if car_infront.a <= 0:
                        self.a = idm(s_desired, delta_s, self.v, self.a_max, self.v_max, self.delta)
                    else:
                        if abs(delta_v)<0.1:
                            self.copy_next_v = True
                            self.a=car_infront.a
                        else:
                            self.a = idm(s_desired, delta_s, self.v, self.a_max, self.v_max, self.delta)
                else:
                    if abs(delta_v)<0.1:
                        self.link = True
                        self.a=car_infront.a
                    else:
                        self.a = idm(s_desired, delta_s, self.v, self.a_max, self.v_max, self.delta)
        
            else:
                delta_s = car_infront.x-self.x-car_infront.l
                delta_v = self.v-car_infront.v 
                s_desired = self.s0
                #s_desired is bigger here because the car infront is a dumb vehicle.
                self.a = idm(s_desired, delta_s, self.v, self.a_max, self.v_max, self.delta)
        
        if not car_infront:
            self.link = False
            self.copy_next_v = False

    def change_color(self):
        if self.copy_next_v:
            self.color = (0, 255, 0)
        elif self.link:
            self.color = (120, 120, 120)
        else:
            self.color = (255, 0, 0)
