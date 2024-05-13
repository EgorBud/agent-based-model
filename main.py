import random
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=3, suppress=True)
a=1/10
n=4
power=10
share_cost=10
birth_cost=100
agents=[]
all_conn=2
energy_cap=0
all_usef=0
class Quantum:
    def __init__(self, a):
        self.inf=a.copy()
class sourse:

    def __init__(self,  q, x, y):
        self.x=x
        self.y=y
        self.power=power
        self.range=1
        self.inf=Quantum(q)
    def shoot(self, aims):
        for aim in aims:
            dist=(aim.x-self.x)**2+(aim.y-self.y)**2
            if dist<self.range:
                aim.new(self.inf, int(self.power*(self.range-dist)))
class agent:
    def __init__(self, x=random.random(), y=random.random(), dad=None):
        global all_conn
        global all_usef
        self.dead=False
        self.quanta = []
        self.moral = np.array([0.0] * n)
        self.energy = 100
        self.useful = 1
        all_usef +=1
        self.hist =[]
        for i in range(n):
            self.moral[i]=random.random()
        self.x=x
        self.y=y
        self.resist=random.random()
        self.age=1
        self.neibours=set()
        for i in agents:
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
        self.energy-=self.age**2/10
        if self.energy >=birth_cost:
            self.energy-=birth_cost
            agents.append(agent(self.x+(random.random()-1/2)/10, self.y+(random.random()-1/2)/10))
        if self.energy<=0:
            #print('dead')

            self.dead=True
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
                    i.share(q, power, self)
                    self.energy-=share_cost
    def share(self, q, power, source):
        self.moral+=(np.array(q.inf)*power)
        power-=1
        if power > 0:
            for i in self.neibours:
                if(i!=source):
                    if self.energy>share_cost:
                        i.new(q, power)
                        self.energy-=share_cost
    def get_neib(self):
        return [(i.x, i.y) for i in self.neibours]
    def neib_count(self):
        return len(self.neibours)

    def show(self):
        print(self.moral, self.energy, self.useful, self.neib_count(), self.x, self.y)
na=40
#neib=4
energy_cap=na*100
all_usef=0


for i in range(na):
    agents.append(agent(random.random(), random.random()))
'''
for i in agents:
    for j in range(neib):
        bro=agents[int(random.random()*na)]
        if(bro!=i):
            i.neibours.add(bro)
            bro.neibours.add(i)
'''
ur=sourse([1, 0,0,0], 1, 1)
ul=sourse([0, 1,0,0], 0, 1)
lr=sourse([0, 0,1,0], 1, 0)
ll=sourse([0, 0,0,1], 0, 0)
sourses=[ur, ul, lr, ll]
time=1000
shoot_pause=3
print(agents)
for i in agents:
    i.show()
plt.scatter([i.x for i in sourses], [i.y for i in sourses], c='r')
plt.scatter([i.x for i in agents], [i.y for i in agents], c='b')
plt.show()
for t in range(time):
    print(t)
    if (t%shoot_pause==0):
        for i in sourses:
            i.shoot(agents)
    for i in agents.copy():
        i.upd()
    agents=list(filter(lambda x: not x.dead, agents))
    plt.scatter([i.x for i in sourses], [i.y for i in sourses], c='r')
    plt.scatter([i.x for i in agents], [i.y for i in agents], c='b')
    plt.draw()
    plt.pause(.001)
    plt.clf()
for i in agents:
    i.show()

plt.scatter([i.x for i in sourses], [i.y for i in sourses], c='r')
plt.scatter([i.x for i in agents], [i.y for i in agents])
plt.draw()

#print(q)