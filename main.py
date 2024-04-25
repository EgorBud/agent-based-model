import random
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=3, suppress=True)
a=1/10
n=4
power=10
cost=10
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

    def __init__(self):
        self.neibours={}
        self.quanta = []
        self.moral = np.array([0.0] * n)
        self.energy = 100
        self.useful = 1
        self.hist =[]
        for i in range(n):
            self.moral[i]=random.random()
        self.x=random.random()
        self.y=random.random()
        self.resist=random.random()
        self.age=1
    def upd(self):
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
        self.useful += learned * self.moral[i]
        self.moral[i] -= learned * self.moral[i]
        self.energy+=self.useful
        self.hist.append(self.useful)
        #self.useful-=self.age*0.6
        self.energy-=self.age*10
        if self.energy<=0:
            print('dead')
            del self
    def new(self, q, power):
        self.moral+=(np.array(q.inf)*power)
        power-=1
        if power > 0:
            for i in self.neibours:
                if self.energy>cost:
                    i.share(q, power, self)
                    self.energy-=cost
    def share(self, q, power, source):
        self.moral+=(np.array(q.inf)*power)
        power-=1
        if power > 0:
            for i in self.neibours:
                if(i!=source):
                    if self.energy>cost:
                        i.new(q, power)
                        self.energy-=cost
    def get_neib(self):
        return [(i.x, i.y) for i in self.neibours.keys()]


    def show(self):
        print(self.moral, self.energy, self.useful)
na=20
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
shoot_speed=1
for t in range(time):
    print(t)
    if (t%shoot_speed==0):
        for i in sourses:
            i.shoot(agents)
    for i in agents:
        i.upd()

for i in agents:
    i.show()
'''
plt.scatter([i.x for i in sourses], [i.y for i in sourses], c='r')
plt.scatter([i.x for i in agents], [i.y for i in agents])
plt.show()
'''
q=agents[int(random.random()*na)].get_neib()
plt.plot(np.exp(np.arange(1, time)/5))
plt.plot(agents[int(random.random()*na)].hist)
plt.show()
print(q)