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
        

        self.colision = {}


    def upgrade(self):
        self.pos = add_lists(self.pos,self.v)
        self.v = add_lists(self.v,self.a)

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

   