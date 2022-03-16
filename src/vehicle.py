import numpy as np

def idm(self, s_desired, delta_s):
        a_freeroad = self.a_max*(1-(self.v/self.v_max)**self.delta) 
        a_interaction = -self.a_max*(s_desired/delta_s)**2
        self.a = a_freeroad + a_interaction

class Vehicle:
    def __init__(self, route, config={}):
        # Set default configuration
        self.set_default_config()
        
        self.route = route
        
        #For smart vehicles. These can only be true if the vehicle is smart:
        self.smart = False
        self.link = False
        self.copy_next_v = False

        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        #Parameters for idm: 
        self.l = 4              # length of vehicle i
        self.s0 = 4             # min desired distance between vehicle i and i-1 
        self.T = 2              # Reaction time of vehicle i's driver. Set to 0 when self.smart==True.
        self.delta = 4          # smoothness of the acceleration
        self.v_max = 16.6       # max desired speed of vehicle i. Set this as road.v_limit?
        self.a_max = 1.44       # Max accel of vehicle i    # 4s
        self.b_max = 4.61       # comfortable deceleration of vehicle i

        self.x = 0
        self.v = self.v_max
        self.a = 0
        self.stopped = False
        
    #Need to decide how we should do it with road and car_infront. Maybe remove car_infront, change to 
    #vehicles_on_road[i-1], and change if car_infront==None to if self.index==0 
    #(where self.index is the vehicles index on the road).
    def update(self, dt, car_infront=None):  
        #update of v, p and a if vehicle is linked
        if self.link:
            self.v = car_infront.v
            self.x += self.v*dt + self.a*(dt**2)/2
            self.a = car_infront.a         
            
            #Need to figure out what to do when vehichle and car_infront, link True, change roads. 
            #Should we always keep track of car_infront based on cars on route? Difficult to know what the order
            #of cars on a arbitrary road will be.
            
        else:
            #update velocity and position
            if self.copy_next_v:
                self.v = car_infront.v
                self.x += self.v*dt + self.a*(dt**2)/2
                self.copy_next_v = False
            
            elif self.v + self.a*dt < 0:
                self.x -= (1/2)*(self.v**2)/self.a
                self.v = 0
                
            else:
                self.v += self.a*dt
                self.x += self.v*dt + self.a*(dt**2)/2
            
            #update acceleration:
            if car_infront==None:
                self.a = self.a_max*(1-(self.v/self.v_max)**self.delta) #a_freeroad
            elif self.smart and car_infront.smart: 
                delta_s = car_infront.x-self.x-car_infront.l
                delta_v = self.v-car_infront.v 
                s_desired = self.s0 #s_desired can be this small because we copy the car infront
                
                if delta_s-s_desired > 0.2:
                    if car_infront.a <= 0:
                        idm(self,s_desired,delta_s)
                    else:
                        if abs(delta_v)<0.1:
                            self.copy_next_v = True
                            self.a=car_infront.a
                        else:
                            idm(self,s_desired,delta_s)
                else:
                    if abs(delta_v)<0.1:
                        self.link = True
                        self.a=car_infront.a
                    else:
                        idm(self,s_desired,delta_s)
        
            else:
                delta_s = car_infront.x-self.x-car_infront.l
                delta_v = self.v-car_infront.v 
                s_desired = self.s0+self.v*self.T+self.v*(delta_v)/(2*np.sqrt(self.a_max*self.b_max))
                #s_desired is bigger here because the car infront is a dumb vehicle.
                idm(self,s_desired,delta_s)
        

        # Common for all 
        if self.x >= self.route.cur_road.length:
            return ("traversed_road", self)



#Suggestions for traffic lights:
#only vehicles_on_road[0] needs to care about stopping before the traffic light.
#all the cars behind will slow down as the car infront is slowing down. 

'''
if self.index==0:
    if self.in_slow_down_zone:
        if traffic_light == green:
            #Regular acc. 

        if traffic light == red:
            self.a = #use damping equation like Bilal here?
'''

        #do it like this?: if the light is green when the car first enters the slow down zone, 
        #it will drive through even if the light changes. If the light is red when it first enters,
        #it will speed up when it changes.
        
        #NOTE: instead of yellow_from_red and yellow_from_green, the vehicle should should just 
        #see either red or green, which will make it either slow down or drive through. If we want yellow light, 
        #that only matters for the animation. This way we don't need to use the damping equation either
        
        
'''
Possible way to solve both traffic light and car_infront question from above, and clean up code:
Always have vehicle in vehicles on road[0]. When the light is green, set position infinity away,
when the light is red, set position at end of road and velocity zero. Then we will get traffic light behavior,
and we can remove car_infront from above and clean up some code. Still the question remains:
what is the best way to have cars switch roads? have to remember removing links between smart cars, changing
which vehicle is in front, etc. Maybe we should just start with vehicles only being able to drive straight 
through an intersection?
'''
