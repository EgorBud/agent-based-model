import random
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=3, suppress=True)

n=4
power=10
class Quantum:

    def __init__(self, a):
        self.inf=a.copy()
class sourse:

    def __init__(self,  q, x, y):
        self.x=x
        self.y=y
        self.power=power
        self.inf=Quantum(q)
    def shoot(self, aims):
        aim=max(aims, key=lambda aim:(aim.x-self.x)**2+(aim.y-self.y)**2)
        aim.new(self.inf, self.power)
class agent:

    def __init__(self):
        self.neibours={}
        self.quanta = []
        self.moral = np.array([0.0] * n)
        for i in range(n):
            self.moral[i]=random.random()
        self.x=random.random()
        self.y=random.random()
        self.resist=random.random()
    def upd(self):
        for i in self.quanta:
            self.moral+=np.array(i[0].inf)*self.resist
            i[1]-=1
        self.quanta=[i for i in self.quanta if i[1] != 0]
    def new(self, q, power):
        self.quanta.append([q, power])
        power-=1
        if power!=0:
            for i in self.neibours:
                trust=1/2-np.linalg.norm(self.moral/np.linalg.norm(self.moral)-i.moral/np.linalg.norm(i.moral))/n
                self.neibours[i]+=trust
                if(self.neibours[i]<0):
                    del self.neibours[i]
                i.not_share(q, power, self, trust)

    def share(self, q, power, sourse, trust):
        self.neibours[sourse]+=trust
        if (self.neibours[sourse] < 0):
            del self.neibours[sourse]
        self.quanta.append([q, power])
        power-=1
        if power!=0:

            for i in self.neibours:
                trust=1/2-np.linalg.norm(self.moral/np.linalg.norm(self.moral)-i.moral/np.linalg.norm(i.moral))/n
                self.neibours[i]+=trust
                if(self.neibours[i]<0):
                    del self.neibours[i]
                i.share(q, power, self, trust)
    def not_share(self, q, power, sourse, trust):
        self.neibours[sourse]+=trust
        if (self.neibours[sourse] < 0):
            del self.neibours[sourse]
        self.quanta.append([q, power])
        power-=1
    def get_neib(self):
        return [(i.x, i.y) for i in self.neibours.keys()]

    def show(self):
        print(n*self.moral/self.moral.sum())
na=50
neib=4

agents=[agent() for i in range(na)]
for i in agents:
    for j in range(neib):
        bro=agents[int(random.random()*na)]
        i.neibours[bro]=1
        bro.neibours[i]=1
ur=sourse([1, 0,0,0], 1, 1)
ul=sourse([0, 1,0,0], 0, 1)
lr=sourse([0, 0,1,0], 1, 0)
ll=sourse([0, 0,0,1], 0, 0)
sourses=[ur, ul, lr, ll]
time=50
shoot_speed=3
for t in range(time):
    print(t)
    if (t%shoot_speed==0):
        for i in sourses:
            i.shoot(agents)
    for i in agents:
        i.upd()
for i in agents:
    i.show()

plt.scatter([i.x for i in sourses], [i.y for i in sourses], c='r')
plt.scatter([i.x for i in agents], [i.y for i in agents])
plt.show()
q=agents[int(random.random()*na)].get_neib()
print(q)