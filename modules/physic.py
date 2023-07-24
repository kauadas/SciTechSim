import math
import time

pi = math.pi
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

class vector:
    def __init__(self,*args):
        self.values = args

    def __add__(self,other):
        if isinstance(other,vector):
            return vector(*[x + y for x,y in zip(self.values,other.values)])

        elif isinstance(other,int):
            return vector(*[x + other for x in self.values])

    def __mul__(self,other):
        if isinstance(other,vector):
            return vector(*[x * y for x,y in zip(self.values,other.values)])

        elif isinstance(other,int):
            return vector(*[x * other for x in self.values])

    def __truediv__(self,other):
        if isinstance(other,vector):
            return vector(*[x / y for x,y in zip(self.values,other.values)])

        elif isinstance(other,int):
            return vector(*[x / other for x in self.values])

    def __pow__(self,other):
        if isinstance(other,vector):
            return vector(*[x ** y for x,y in zip(self.values,other.values)])

        elif isinstance(other,int):
            return vector(*[x ** other for x in self.values])

    def abs(self):
        pass


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
        
        self.P = kwargs,get("P")
        self.I = self.P / 4*pi
        self.origin = kwargs.get("origin",[0,0,0])
        self.V = kwargs.get("V",C)
        self.E = H*self.V/self.A
        self.R = 0

    def upgrade(self):
            self.R += self.V
            self.I = self.P / 4*pi*self.R**2



def calc(gradient: list,V: list,p,Fbody: list,u):
    Ap = [i*p for i in gradient]

    nAp = [i*-1 for i in Ap]

    uA2 = [u*(i**2) for i in gradient]

    uA2v = [i*i2 for i,i2 in zip(uA2,V)]

    p1 = add_lists(nAp, uA2v)

    return add_lists([p*i for i in Fbody],p1)

