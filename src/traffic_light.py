from vehicle import Vehicle
from simulation import Simulation

from road import Road
from simulation import Simulation

class TrafficLights:
    light = {0:'Red', 1:'Green'}

    def __init__(self, roads):
        self.pos = road.end() 
        self.cycle_index = 0
<<<<<<< main
        self.cycles_dict = {1:(True,False) , 2:((True,False),(False,True))} ## Er dette felles for alle trafikklys
        self.cycle = self.cycles_dict[len(roads)]
        self.maxtime = 60*5 #5 sek ved 60 fps :^)
    def change_light(self):
        if get_time() % self.maxtime <= 1e-10:
            cycle_index += 1
        return cycle_index % len(self.cycle)

    def get_time(): ## Får tiden fra simulation.
=======
        self.cycles = {1:(True,False) , 2:((True,False),(False,True))} ## Er dette felles for alle trafikklys
        self.cycle = self.cycles[len(roads)]
    def change_light(self):
        if get_time() % self.maxtime <= 1e-6:
            cycle_index += 1
        return cycle_index % len(self.cycle)

    def get_time():
>>>>>>> TrafficLights coordinates traffic lights
        return Simulation.t

    def update(self):
        change_light()
        return self.cycle[cycle_index]
<<<<<<< main

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
=======
>>>>>>> TrafficLights coordinates traffic lights
