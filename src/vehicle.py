import numpy as np

class Vehicle:
    def __init__(self, route, time):  
        self.spawn_time = time  # Time the vehicle spawns
        self.route = route
        self.full_dist = np.sum([road.length for road in route.roads]) # Length of all roads on route
        self.traversed_dist = 0

        self.l = 4              # length of vehicle i

        self.a_max = 2          # Max accel of vehicle i    # 4s
        self.b_max = 4.61       # comfortable deceleration of vehicle i
        self.v_max = 16.6       # max desired speed of vehicle i. Set this as road.v_limit?
        
        self.x = 0
        self.v = self.v_max
        self.a = 0

        self.link = False
        self.copy_next_v = False

        self.run_this_light = False
    
    def get_traversed_dist(self):
        return self.traversed_dist + self.x

    def control_acceleration(self, car_infront, light):
        if not light:
            self.run_this_light = False
            self.normal_acceleration(car_infront)
            return
        in_stop_zone = (self.route.cur_road.length - self.x <= light.stop_zone)
        if not in_stop_zone:
            self.normal_acceleration(car_infront)
            return
        if in_stop_zone and light.is_green:
            if self.v >= 10: self.run_this_light = True
            self.normal_acceleration(car_infront)
            return
        if in_stop_zone and not light.is_green and self.run_this_light:
            self.normal_acceleration(car_infront)
            return
        """Fungerer ikke, er tiltenkt for å stoppe casen hvor biler kommer veeeldig nærme hverandre ved rødt lys
        if car_infront:
            if in_stop_zone and not light.is_green and not car_infront.run_this_light and car_infront.route.cur_road == self.route.cur_road:
                self.normal_acceleration(car_infront)
                return
        """
        if car_infront and not light.is_green and in_stop_zone:
            if car_infront.run_this_light and car_infront.route.cur_road == self.route.cur_road:
                self.damping()
                return
            if car_infront.route.cur_road == self.route.cur_road:
                self.normal_acceleration(car_infront)
                return

        if in_stop_zone and not light.is_green and not self.run_this_light:
            self.damping()
            return
        self.normal_acceleration(car_infront)
        return

    def damping(self):
        # Denne burde egentlig drive avstand fra trafikklys mot null.
        x_e = self.x - (self.route.cur_road.length - 5)
        v_e = self.v
        
        # Tune dette
        self.a = max(-(1*x_e + 1.1*2*v_e), -self.b_max)

        # Dette må refaktoreres i framtiden, dette er hacky fix fordi update_physics sjekker if self.link
        self.link = False

    def normal_acceleration(self, car_infront):
        pass

    def idm(self, s_desired, delta_s):
        a_freeroad = self.a_max*(1-(self.v/self.v_max)**self.delta) 
        a_interaction = -self.a_max*(s_desired/delta_s)**2
        return a_freeroad + a_interaction

    def update_physics(self, dt, car_infront):
        if self.link and car_infront:
            self.v = car_infront.v
            self.x += self.v*dt + self.a*(dt**2)/2      
            
        else:
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

    def change_color(self, car_infront):
        pass
    
    def update(self, dt, car_infront=None, light=None):
        self.control_acceleration(car_infront, light)

        if self.smart:
            self.set_state()

        self.update_physics(dt,car_infront)
        
        self.change_color(car_infront)

        # Common for all 
        if self.x >= self.route.cur_road.length:
            return ("traversed_road", self)



class DumbVehicle(Vehicle):
    def __init__(self, route, time, config={}):
        super().__init__(route, time)

        #Parameters for idm: 
        self.T = 1              # Reaction time of vehicle i's driver. Set to 0 when self.smart==True.
        self.delta = 4          # smoothness of the acceleration
        self.s0 = 8             # min desired distance between vehicle i and i-1. 
        #!!Note: s0 needs to be bigger than car_infront.l, or else the desired distance is inside the vehicle in front.
        #Also: Want to change self.s0 to 2*car_infront.l for dumb vehicle, and 1.5*car_infront.l for smart vehicle.

        self.smart = False

        self.color = (255, 0, 0)

        for key, attr in config.items():
            setattr(self, key, attr)

    def normal_acceleration(self, car_infront):
        if car_infront:
            delta_s = car_infront.x-self.x-car_infront.l
            delta_v = self.v-car_infront.v 
            s_desired = self.s0+self.v*self.T+self.v*(delta_v)/(2*np.sqrt(self.a_max*self.b_max))
            self.a = self.idm(s_desired,delta_s)
        else:
            self.a = self.a_max*(1-(self.v/self.v_max)**self.delta) 

    
    
class SmartVehicle(Vehicle):
    def __init__(self, route, time, config={}):
        super().__init__(route, time)

        #Parameters for idm: 
        self.T = 0             # Reaction time of vehicle i's driver. Set to 0 when self.smart==True.
        self.delta = 4          # smoothness of the acceleration
        self.s0 = 6            # min desired distance between vehicle i and i-1 
        self.link_window = 4

        self.smart = True
        self.state = "init"

        self.color = (255, 0, 0)

        for key, attr in config.items():
            setattr(self, key, attr)

    def normal_acceleration(self, car_infront):
        if car_infront==None:
            self.a = self.a_max*(1-(self.v/self.v_max)**self.delta)
            if self.link:
                self.link=False #Need this incase vehicle is linked to car_infront, but then car_infront leaves road.
            return
        
        delta_s = car_infront.x-self.x-car_infront.l
        delta_v = self.v-car_infront.v 
        s_desired = self.s0+self.v*(delta_v)/(2*np.sqrt(self.a_max*self.b_max))
        
        if self.link:
            self.a = car_infront.a         
        elif self.smart and car_infront.smart: 
            s_desired = self.s0 + self.v*(delta_v)/(2*np.sqrt(self.a_max*self.b_max))
    
            if delta_s-s_desired <= 0.2:
                if abs(delta_v)<0.1:
                    self.link = True
                    self.a=car_infront.a
                    self.state = "linked"
                else:
                    self.a = self.idm(s_desired,delta_s)
            else:    
                if car_infront.a <= 0:
                    self.a = self.idm(s_desired,delta_s)
                else:
                    if abs(delta_v)<0.1:
                        self.copy_next_v = True
                        self.a=car_infront.a
                    else:
                        self.a = self.idm(s_desired,delta_s)
        else:
            self.a = self.idm(s_desired+car_infront.l,delta_s)
    
    def set_state(self):
        if self.link:
            self.state = "linked"
        elif self.copy_next_v:
            self.state = "copy_next_v"
        elif self.smart:
            self.state = "init"

    def change_color(self,car_infront):
        if self.state == "linked":
            self.color = (0, 255, 0)
        elif self.state == "copy_next_v":
            self.color = (0, 0, 255)
        elif car_infront:
            self.color = (0, 0, 255)
        else:
            self.color = (0,0,255)