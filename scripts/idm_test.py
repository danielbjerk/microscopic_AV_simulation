from vehicle import Vehicle
import matplotlib.pyplot as plt


#For testing
class Road:
    def __init__(self) -> None:
        self.v_limit=3
    
road=Road()


#Smart cars:
smartcar1 = Vehicle()
smartcar1.smart = True
smartcar1.T = 0
smartcar1.x=15
smartcar1.v=0
smartcar1.plist[0]=smartcar1.x
smartcar1.vlist[0]=smartcar1.v


smartcar2 = Vehicle()
smartcar2.smart = True
smartcar2.T = 0
smartcar2.x=5
smartcar2.v=0
smartcar2.plist[0]=smartcar2.x
smartcar2.vlist[0]=smartcar2.v

smartcar3 = Vehicle()
smartcar3.smart = True
smartcar3.T = 0
smartcar3.x=0
smartcar3.v=3
smartcar3.plist[0]=smartcar3.x
smartcar3.vlist[0]=smartcar3.v

#Animation
time=0
tlist = [time]
dt=0.1
while time<10:
    plt.xlim(0,40)
    plt.scatter(smartcar1.x,0,color="blue")
    plt.scatter(smartcar2.x,0,color="red")
    plt.scatter(smartcar3.x,0,color="green")
    plt.draw()
    plt.pause(0.000001)
    plt.clf()
    
    smartcar1.update_acc(road,dt)
    smartcar2.update_acc(road,dt,smartcar1)
    smartcar3.update_acc(road,dt,smartcar2)
    
    time += dt
    tlist.append(time)
    
    print(time)
    print("1 linked:",smartcar1.link)
    print("2 linked:",smartcar2.link)
    print("3 linked:",smartcar3.link)
    print("2 copy_next_v:",smartcar2.copy_next_v)
    print("3 copy_next_v:",smartcar3.copy_next_v)
    print("1 speed:", smartcar1.v)
    print("2 speed:", smartcar2.v)
    print("3 speed:", smartcar3.v)
    
    #plt.pause(0.3)

#Graph
plt.plot(tlist, smartcar1.plist, 'blue', label='car1_pos(t)')
plt.plot(tlist, smartcar1.vlist, 'b--', label='car1_vel(t)')
plt.plot(tlist, smartcar2.plist, 'red', label='car2_pos(t)')
plt.plot(tlist, smartcar2.vlist, 'r--', label='car2_vel(t)')
plt.plot(tlist, smartcar3.plist, 'green', label='car3_pos(t)')
plt.plot(tlist, smartcar3.vlist, 'g--', label='car3_vel(t)')


plt.legend(loc='best')
plt.xlabel('t')
plt.grid()
plt.show()

#Dumb cars:
car1 = Vehicle()
car1.x=10
car1.v=0
car1.plist[0]=car1.x
car1.vlist[0]=car1.v

car2 = Vehicle()
car2.x=5
car2.v=1
car2.plist[0]=car2.x
car2.vlist[0]=car2.v

car3 = Vehicle()
car3.x=0
car3.v=2
car3.plist[0]=car3.x
car3.vlist[0]=car3.v

#Animation:
time=0
tlist = [time]
dt=0.1
i=0
while time<10:
    clear_output(wait=True)
    plt.xlim(0,35)
    plt.scatter(car1.x,0,color="blue")
    plt.scatter(car2.x,0,color="red")
    plt.scatter(car3.x,0,color="green")
    plt.draw()
    plt.pause(0.000001)
    plt.clf()
    
    car1.update_acc(road,dt)
    car2.update_acc(road,dt,car1)
    car3.update_acc(road,dt,car2)
    time += dt
    tlist.append(time)


#Plotting:
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

