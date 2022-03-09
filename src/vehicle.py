from scipy.integrate import ode
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import clear_output

""" Main under

import numpy as np

class Vehicle:
    def __init__(self, route, config={}):
        # Set default configuration
        self.set_default_config()

        self.route = route

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()

    def set_default_config(self):    
        self.l = 4
        self.s0 = 4
        self.T = 1
        self.v_max = 16.6
        self.a_max = 1.44
        self.b_max = 4.61

        self.path = []
        self.current_road_index = 0

        self.x = 0
        self.v = self.v_max
        self.a = 0
        self.stopped = False

    def init_properties(self):
        self.sqrt_ab = 2*np.sqrt(self.a_max*self.b_max)
        self._v_max = self.v_max

    def update(self, lead, dt):
        # Update position and velocity
        if self.v + self.a*dt < 0:
            self.x -= 1/2*self.v*self.v/self.a
            self.v = 0
        else:
            self.v += self.a*dt
            self.x += self.v*dt + self.a*dt*dt/2 # Hvorfor ikke bytte om på disse?
        
        # Update acceleration
        alpha = 0
        if lead:
            delta_x = lead.x - self.x - lead.l # Denne er motsatt av hva han skriver i artikkelen.
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)

        if self.stopped: 
            self.a = -self.b_max*self.v/self.v_max

        if self.x >= self.route.cur_road.length:
            return ("traversed_road", self)
        
    def stop(self):
        self.stopped = True

    def unstop(self):
        self.stopped = False

    def slow(self, v):
        self.v_max = v

    def unslow(self):
        self.v_max = self._v_max
        

"""

class Vehicle:
    def __init__(self) -> None:
        #Current vehicle has index i, car infront has index i-1
        
        self.passengers = 0
        self.pos_percentage = 0
        
        self.smart = False
        
        self.at_target = False

        #self.route = calculate_route()
        
        self.p = 0
        self.v = 0
        self.a = 0
        
        self.plist = [self.p] #So we can plot graphs
        self.vlist = [self.v]
        
    
        self.l = 0.5 #length of vehicle i
        self.s0 = 1 #min desired distance between vehicle i and i-1 
        self.v0 = 3 #max desired speed of vehicle i. Set this as road.v_limit?
        self.delta = 2 #smoothness of the acceleration
        self.T = 0.5 #Reaction time of vehicle i's driver
        self.amax = 4 #Max accel of vehicle i
        self.b = 3 #comfortable deceleration of vehicle i
         

    def update_ftl(self, road, dt, car_infront=None):
        self.v += self.a*dt
        self.p += self.v*dt + self.a*(dt**2)/2 #Notice: Uses the updated speed
        
        if car_infront==None:
            self.a=0
        elif (car_infront.p-self.p)>5:       
            self.a = 1-self.v/road.v_limit               
        else:                            
            self.a = (car_infront.v-self.v)/(car_infront.p-self.p)
            
        self.plist.append(self.p)
        self.vlist.append(self.v)
        
    def update_idm(self,road,dt,car_infront=None):  #Later: Change car_infront to vehicle[self.index-1] from roads
        self.v += self.a*dt
        self.p += self.v*dt + self.a*(dt**2)/2
        
        if car_infront==None:
            self.a=0
        else:
            delta_s = self.p-car_infront.p-self.l #Distance from bumper to bumper between vehicle i and i-1. 
            delta_v = self.v-car_infront.v #Difference in velocity between vehicle i and i-1. Notice: Negative if vehicle i has higher speed than i-1.
            s_desired = self.s0+self.v*self.T+self.v*(delta_v)/np.sqrt(2*self.amax*self.b) #desired distance between vehicle i and i-1        
        
            #Let's do like Bilal, and split the acc into a = a_freeroad + a_interaction terms,
            #as this could be useful when considering smart vehicles.
            
            a_freeroad = self.amax*(1-(self.v/self.v0)**self.delta) 
            a_interaction = -self.amax*(s_desired/delta_s)**2

            self.a = a_freeroad + a_interaction
        
        self.plist.append(self.p)
        self.vlist.append(self.v)

if __name__ == "__main__":
    #Testing
    class Road:
        def __init__(self) -> None:
            self.v_limit=3

    car1 = Vehicle()
    car1.p=15
    car1.v=0
    car1.plist[0]=car1.p
    car1.vlist[0]=car1.v

    car2 = Vehicle()
    car2.p=5
    car2.v=0
    car2.plist[0]=car2.p
    car2.vlist[0]=car2.v

    car3 = Vehicle()
    car3.p=0
    car3.v=1
    car3.plist[0]=car3.p
    car3.vlist[0]=car3.v

    road=Road()

    time=0
    tlist = [time]
    dt=0.1
    while time<10:
        
        '''
        clear_output(wait=True)
        plt.xlim(0,35)
        plt.scatter(car1.p,0,color="blue")
        plt.scatter(car2.p,0,color="red")
        plt.scatter(car3.p,0,color="green")
        plt.draw()
        plt.pause(0.000001)
        plt.clf()
        '''
        
        car1.update_idm(road,dt)
        car2.update_idm(road,dt,car1)
        car3.update_idm(road,dt,car2)
        
        time += dt
        tlist.append(time)

    plt.plot(tlist, car1.plist, 'blue', label='car1_pos(t)')
    plt.plot(tlist, car1.vlist, 'b--', label='car1_vel(t)')
    plt.plot(tlist, car2.plist, 'red', label='car2_pos(t)')
    plt.plot(tlist, car2.vlist, 'r--', label='car2_vel(t)')
    plt.plot(tlist, car3.plist, 'green', label='car3_pos(t)')
    plt.plot(tlist, car3.vlist, 'g--', label='car3_vel(t)')


    plt.legend(loc='best')
    plt.xlabel('t')
    plt.grid()
    plt.show()

