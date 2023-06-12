import math
import time

G = 6.674*(10**-11)
K = 9*(10**9)
H = 6.62607015*(10**-36)
C = 299792458

# soma duas listas
def add_lists(list1: list, list2: list):
    return [x + y for x,y in zip(list1,list2)]


# subtrai duas listas

def subtract_lists(list1: list, list2: list):
    return [x - y for x,y in zip(list1,list2)]

#calcula o modulo do vetor
def abs_vector(x: list):
    y = 0
    for i in x:
        y += i**2

    return math.sqrt(y)

#classe pai body representa corpos físicos
class body:
    def __init__(self,**kwargs):
        self.m = kwargs.get("m", 0)
        self.Q = kwargs.get("Q", 0)
        self.pos = kwargs.get("pos", [0, 0, 0])
        self.v = kwargs.get("v", [0, 0, 0])
        self.a = kwargs.get("a", [0, 0, 0])

        self.angle = kwargs.get("angle", [0, 0, 0])
        self.aV = kwargs.get("angular_velocity", [0, 0, 0])
        self.aA = kwargs.get("angular_aceleration", [0, 0, 0])
        

        self.colision = {}


    def upgrade(self):
        self.pos = add_lists(self.pos,self.v)
        self.v = add_lists(self.v,self.a)
        self.angle = add_lists(self.angle,self.aV)
        self.aV = add_lists(self.aV,self.aA)

    def is_collide(self,obj2):
        for key,value in self.colision.items():
            pass

class ambient:
    def __init__(self,**kwargs):
        self.objects = []

        self.G = kwargs.get("G",G)
        self.K = kwargs.get("K",K)
        self.time = kwargs.get("time",1)

    def upgrade(self):
        pass

        

def to_vector(i: float,ab: list):
    abs_ab = abs_vector(ab)

    nAB = [x/abs_ab for x in ab]

    Y = [i*x for x in nAB]

    return Y


class wave:
    def __init__(self,**kwargs):
        self.a = kwargs.get("a")
        self.T = kwargs.get("T")
        self.A = kwargs.get("A",2)
        self.E = H*C/self.A
        self.P = self.a * self.T/2
        self.i = self.P
        self.origin = kwargs.get("origin",[0,0,0])
        self.V = kwargs.get("V",C)
        self.R = 0

    def upgrade(self):
        self.i *= 1/self.R**2
        self.R += self.V