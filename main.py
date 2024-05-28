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
birth_cost=200
agents=[]
all_conn=2
energy_cap=0
all_usef=0
def angle(v1, v2):
    n1=(np.linalg.norm(v1))
    n2=(np.linalg.norm(v2))
    if(n1==0)or (n2==0):
        return 0
    v1_u = v1/n1
    v2_u = v2/n2
    return (np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))+1
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
                aim.new(self.inf, int(self.func(t)*self.power/(1+dist)))
class agent:
    def __init__(self, x=random.random(), y=random.random(), dad=None, moral=np.array([0.0] * n), knowlege=np.array([0.0] * n), type=1):
        global all_conn
        global all_usef
        self.type=type
        self.dead=False
        self.moral = np.array(moral.copy())
        self.energy = 100
        self.useful = 1
        all_usef +=1
        self.hist =[]
        self.knowlege = np.array(knowlege.copy())
        self.x=x
        self.y=y
        self.resist=1
        self.age=1
        self.neibours=set()
        for i in agents:
            if(i!=self) and (i not in self.neibours):
                p = i.neib_count() * angle(self.knowlege, i.knowlege) / all_conn

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
        b=self.moral.sum()
        self.age+=1

        '''
        for i in range(len(self.moral)):
            learned=(1/(1+np.exp(-2*a*(n*self.moral[i]-b))))
            self.useful+=learned*self.moral[i]
            self.moral[i]-=learned*self.moral[i]
        '''
        i=np.argmax(self.moral)
        learned = (1 / (1 + np.exp(-2 * a * (n * self.moral[i] - b))))
        #print('l', learned)
        self.useful += learned * self.moral[i]
        all_usef += learned * self.moral[i]
        self.knowlege[i]+=learned * self.moral[i]
        self.moral[i] -= learned * self.moral[i]
        #print('moral', self.moral[i])

        self.energy+=min(self.useful, energy_cap*self.useful/all_usef)
        self.hist.append(self.useful)
        #self.useful-=self.age*0.6
        if(len(self.neibours)==0):
            for i in agents:
                if (i != self)  and (i not in self.neibours):
                    p=i.neib_count()*angle(self.knowlege, i.knowlege)/all_conn
                    if(random.random()<p):
                        i.neibours.add(self)
                        self.neibours.add(i)
                        all_conn=all_conn+2
        self.energy-=self.age**2/10

        if self.energy >=birth_cost:
            self.energy-=birth_cost
            agents.append(agent(self.x+(uniform.rvs()-1/2)/10, self.y+(uniform.rvs()-1/2)/10, self,self.moral/10, self.knowlege/10, self.type))
        if self.energy<=0:

            self.dead=True
            all_usef-=self.useful
            for i in self.neibours:
                all_conn-=2
                i.neibours.remove(self)
            self.neibours.clear()

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
        print(self.moral, self.knowlege, self.energy, self.useful, self.neib_count(), self.x, self.y)
nb=50
ng=50
na=nb+ng
energy_cap=na*100
all_usef=0
agents.append(agent(random.random(), random.random(), moral=[1, 0,0, 0], knowlege=[100, 0, 0, 0], type='b'))
agents.append(agent(random.random(), random.random(), moral=[0, 1,0, 0], knowlege=[0, 100, 0, 0], type='g'))
agents[0].neibours.add(agents[1])
agents[1].neibours.add(agents[0])

for i in range(min(nb-1, ng-1)):
    agents.append(agent(random.random(), random.random(), moral=[1, 0, 0, 0], knowlege=[100, 0, 0, 0], type='b'))
    agents.append(agent(random.random(), random.random(), moral=[0, 100, 0, 0], knowlege=[0, 100, 0, 0], type='g'))
if(max(nb, ng)==nb):
    ty='b'
else:
    ty='g'
for i in range(min(nb-1, ng-1), max((nb-1, ng-1))):
    agents.append(agent(random.random(), random.random(), moral=[0, 100, 0, 0], knowlege=[0, 100, 0, 0], type=ty))


def fun(t):
    return np.sin(t)+2
ur=sourse([1, 0,0,0], 1, 1, 10, fun)
ul=sourse([0, 1,0,0], 0, 1, 10, fun)
lr=sourse([0, 0,1,0], 1, 0, 10, fun)
ll=sourse([0, 0,0,1], 0, 0, 10, fun)
sourses=[ur, ul, lr, ll]
time=500
shoot_pause=1

plt.scatter([i.x for i in sourses], [i.y for i in sourses], c='r')
for i in agents:
    plt.scatter(i.x , i.y, c=i.type)
plt.show()
print(all_conn)
for t in range(time):
    print(t)
    if (t%shoot_pause==0):
        for i in sourses:
            i.shoot(agents, t)
    for i in agents.copy():
        i.upd()
    agents=list(filter(lambda x: not x.dead, agents))
    plt.clf()
    plt.scatter([i.x for i in sourses], [i.y for i in sourses], c='r')
    for i in agents:
        plt.scatter(i.x, i.y, c=i.type)

    plt.draw()
    '''
    ani = animation.FuncAnimation(plt, animate, repeat=True,
                                  frames=time - 1, interval=50)
    '''
    plt.pause(.001)
    plt.clf()
print(len(agents))
for i in agents:
    #print(i.neibours)
    1
    #i.show()

plt.scatter([i.x for i in sourses], [i.y for i in sourses], c='r')
plt.scatter([i.x for i in agents], [i.y for i in agents])
plt.show()

#print(q)