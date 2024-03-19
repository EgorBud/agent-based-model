import random
import numpy as np
import matplotlib.pyplot as plt


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
        self.inf=q
    def shoot(self, aims):
        aim=max(aims, key=lambda aim:(aim.x-self.x)**2+(aim.y-self.y)**2)
        aim.new(Quantum(self.inf), self.power)
class agent:

    def __init__(self):
        self.neibours=[]
        self.quanta = []
        self.moral = np.array([0.0] * n)
        for i in range(n):
            self.moral[i]=random.random()
        self.x=random.random()
        self.y=random.random()
    def upd(self):
        for i in self.quanta:
            self.moral+=np.array(i[0].inf)
            i[1]-=1
        self.quanta=[i for i in self.quanta if i[1] != 0]
    def new(self, q, power):
        self.quanta.append([q, power])
        power-=1
        if power!=0:
            for i in self.neibours:
                i.new(q, power)
    def show(self):
        print(n*self.moral/self.moral.sum())
na=40
neib=1

agents=[agent() for i in range(na)]
for i in agents:
    i.neibours=[agents[int(random.random()*na)] for j in range(neib)]
ur=sourse([1, 0,0,0], 1, 1)
ul=sourse([0, 1,0,0], 0, 1)
lr=sourse([0, 0,1,0], 1, 0)
ll=sourse([0, 0,0,1], 0, 0)
sourses=[ur, ul, lr, ll]
time=40
for t in range(time):
    print(t)
    for i in sourses:
        i.shoot(agents)
    for i in agents:
        i.upd()
for i in agents:
    i.show()

plt.scatter([i.x for i in sourses], [i.y for i in sourses], c='r')
plt.scatter([i.x for i in agents], [i.y for i in agents])
plt.show()