import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import uniform
import matplotlib.animation as animation

np.set_printoptions(precision=3, suppress=True)
a=1/10
n=4
power=10
share_cost=10
birth_cost=150
agents=[]
all_conn=2
energy_cap=0
all_usef=0
class Quantum:
    def __init__(self, a):
        self.inf=a.copy()
class sourse:

    def __init__(self,  q, x, y, power=power, func=lambda x:1):
        self.x=x
        self.y=y
        self.power=power
        self.range=1
        self.inf=Quantum(q)
        self.func=func
    def shoot(self, aims, t=0):
        for aim in aims:
            dist=(aim.x-self.x)**2+(aim.y-self.y)**2
            if dist<self.range:
                aim.new(self.inf, int(self.func(t)*self.power*(self.range-dist)))
class agent:
    def __init__(self, x=random.random(), y=random.random(), dad=None, moral=np.array([0.0] * n)):
        global all_conn
        global all_usef
        self.dead=False
        self.moral = moral
        self.energy = 100
        self.useful = 1
        all_usef +=1
        self.hist =[]

        self.x=x
        self.y=y
        self.resist=1
        self.age=1
        self.neibours=set()
        for i in agents:
            if(i!=self):
                p=i.neib_count()/all_conn
                if(random.random()<p):

                    i.neibours.add(self)
                    self.neibours.add(i)
                    all_conn=all_conn+2
        if(dad!=None):
            self.neibours.add(dad)
            dad.neibours.add(self)

    def upd(self):
        global all_usef
        global all_conn
        b=self.moral.sum()+self.useful
        self.age+=1
        '''
        for i in range(len(self.moral)):
            learned=(1/(1+np.exp(-2*a*(n*self.moral[i]-b))))
            self.useful+=learned*self.moral[i]
            self.moral[i]-=learned*self.moral[i]
        '''
        i=np.argmax(self.moral)
        learned = (1 / (1 + np.exp(-2 * a * (n * self.moral[i] - b))))
        self.useful += learned * self.moral[i]
        all_usef += learned * self.moral[i]
        self.moral[i] -= learned * self.moral[i]
        self.energy+=min(self.useful, energy_cap*self.useful/all_usef)
        self.hist.append(self.useful)
        #self.useful-=self.age*0.6
        if(len(self.neibours)==0):
            for i in agents:
                if (i != self):
                    p=i.neib_count()/all_conn
                    if(random.random()<p):
                        i.neibours.add(self)
                        self.neibours.add(i)
                        all_conn=all_conn+2
        self.energy-=self.age**2/10
        if self.energy >=birth_cost:
            self.energy-=birth_cost
            agents.append(agent(self.x+(uniform.rvs()-1/2)/10, self.y+(uniform.rvs()-1/2)/10))
        if self.energy<=0:
            #print('dead')

            self.dead=True
            self.neibours.discard(self)
            all_usef-=self.useful
            for i in self.neibours:
                all_conn-=2
                i.neibours.remove(self)
            del self

    def new(self, q, power):
        self.moral+=(np.array(q.inf)*power)
        power-=1
        if power > 0:
            for i in self.neibours:
                if self.energy>share_cost:
                    i.new(q, power)
                    self.energy-=share_cost

    def get_neib(self):
        return [(i.x, i.y) for i in self.neibours]
    def neib_count(self):
        return len(self.neibours)

    def show(self):
        print(self.moral, self.energy, self.useful, self.neib_count(), self.x, self.y)
na=100
def animate(i):
    scat.set_offsets((x[i], 0))
    return scat,

energy_cap=na*100
all_usef=0
agents.append(agent(random.random(), random.random()))
agents.append(agent(random.random(), random.random()))
agents[0].neibours.add(agents[1])
agents[1].neibours.add(agents[0])

for i in range(na-2):
    agents.append(agent(random.random(), random.random()))
def fun(t):
    return np.sin(t)+2
ur=sourse([1, 0,0,0], 1, 1, 10, fun)
ul=sourse([0, 1,0,0], 0, 1, 10, fun)
lr=sourse([0, 0,1,0], 1, 0, 10, fun)
ll=sourse([0, 0,0,1], 0, 0, 10, fun)
sourses=[ur, ul, lr, ll]
time=1000
shoot_pause=3

plt.scatter([i.x for i in sourses], [i.y for i in sourses], c='r')
plt.scatter([i.x for i in agents], [i.y for i in agents], c='b')
plt.show()
for t in range(time):
    print(t)
    if (t%shoot_pause==0):
        for i in sourses:
            i.shoot(agents, t)
    for i in agents.copy():
        i.upd()
    agents=list(filter(lambda x: not x.dead, agents))
    plt.scatter([i.x for i in sourses], [i.y for i in sourses], c='r')
    plt.scatter([i.x for i in agents], [i.y for i in agents], c='b')
    plt.draw()
    '''
    ani = animation.FuncAnimation(plt, animate, repeat=True,
                                  frames=time - 1, interval=50)
    '''
    plt.pause(.001)
    plt.clf()
print(all_conn)
for i in agents:
    #print(i.neibours)
    i.show()

plt.scatter([i.x for i in sourses], [i.y for i in sourses], c='r')
plt.scatter([i.x for i in agents], [i.y for i in agents])
plt.show()

#print(q)