from vehicle import Vehicle
from simulation import Simulation

from road import Road
from simulation import Simulation

class TrafficLight:
    light = {0:'Red', 1:'Green'}

    def __init__(self, road):
        self.road = road
        self.pos = road.end 
        self.cycle_index = 0
        #self.cycles_dict = {1:(True,False) , 2:((True,False),(False,True))} ## Er dette felles for alle trafikklys
        self.cycle = (True, False)#self.cycles_dict[len(road)]
        self.maxtime = 10
    
    def change_light(self, t):
        if t % self.maxtime <= 1e-10:
            self.cycle_index += 1
            self.cycle_index %= len(self.cycle)

    def get_time(): ## Får tiden fra simulation.
        return Simulation.t

    def update(self, t):
        self.change_light(t)
        print(self.cycle[self.cycle_index])
        return self.cycle[self.cycle_index]

'''
    Vi kan finne ut hva maks bremselengde er fra en bil, gitt fart.
    
    For å unngå en skarp bremsing kan en bil beregne komfortabel bremsing 
    og fart for å avgjøre om den rekker å stoppe for rødt lys. Dersom den ikke gjør dette kan 
    den kjøre gjennom. Ellers bør den ha en regel for å stoppe. Påfølgende biler vil derfor også
    stoppe. Traffic manager vet hvor bilene er og deres hastigheter. 
    Traffic manager kan loope fra første til siste vehicle på en vei for å avgjøre 
    om den bør stoppe. Når den finner en bil som er i passende avstand kan den 
    instrueres om å benytte en annen bremseregel. Dette låner seg kanskje godt til gult lys?

'''
