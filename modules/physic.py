import math
import time
from modules.mathematic import *

pi = math.pi
G = 6.674*(10**-11)
K = 9*(10**9)
H = 6.62607015*(10**-36)
C = 299792458
k = 8*pi*G/C**4

# soma duas listas
def add_lists(list1: list, list2: list):
    return [x + y for x,y in zip(list1,list2)]


# subtrai duas listas

def subtract_lists(list1: list, list2: list):
    return [x - y for x,y in zip(list1,list2)]


#classe pai body representa corpos físicos
class body:
    def __init__(self,**kwargs):
        self.id = kwargs.get("id")
        self.m = kwargs.get("m", 0)
        self.Q = kwargs.get("Q", 0)
        self.fric = 0
        self.resultant_forces = {}
        self.pos = vector(*kwargs.get("pos", [0, 0, 0]))
        self.v = vector(*kwargs.get("v", [0, 0, 0]))
        self.a = vector(*kwargs.get("a", [0, 0, 0]))

        self.angle = vector(*kwargs.get("angle", [0, 0, 0]))
        self.aV = vector(*kwargs.get("angular_velocity", [0, 0, 0]))
        self.aA = vector(*kwargs.get("angular_aceleration", [0, 0, 0]))
        

        self.matrix = kwargs.get("matrix",{})




    def upgrade(self):
        
            
        if self.m != 0:
            self.a = sum(list(self.resultant_forces.values()),start=vector(*[0 for i in self.pos]))/self.m

        else:
            self.a = sum(list(self.resultant_forces.values()),start=vector(*[0 for i in self.pos]))

        self.resultant_forces.clear()
        if self.m >> 0 and abs(self.v) + abs(self.a) < C:
            self.v = self.v + self.a

        self.pos = self.pos + self.v
        
        if not self.m >> 0 and abs(self.aV) + abs(self.aA) >= C:
            self.aV = self.aV + self.aA
            
        self.angle = self.angle + self.aV
        
    def apply_force(self,name: str,F):
        self.resultant_forces[name] = F
        

    def is_collide(self,obj2):
        
        for key,value in self.matriz.items():
            for key2,value2 in obj2.matriz.items():
                pass




def create_matrix(size_x: int,size_y: int,value_zero):
        values = []
        for y in range(size_y):
            values.append([])
            for x in range(size_x):
                values[y].append(value_zero)

        return values

class ambient:
    def __init__(self,**kwargs):
        self.objects = {}
        self.universal_forces = []

        self.G = kwargs.get("G",G)
        self.K = kwargs.get("K",K)
        self.time = kwargs.get("time",1)

    def upgrade(self):
        for force in self.universal_forces:
            for obj in self.objects.values():
                force(self,obj)

        for obj in self.objects.values():
            obj.upgrade()

            print(obj.v.values)

        

        

def to_vector(i: float,ab: vector):
    nAB = ab/abs(ab)

    Y = nAB*i

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



def navier_stocks(gradient: vector,V: vector,p,Fbody: vector,u):
    Ap = (gradient*p)*-1

    uA2 = (gradient**2)*u

    uA2v = V*uA2

    p1 = Ap + uA2v

    return Fbody*p + p1


class Wave_Particle:
    def __init__(self,**kwargs):
        self.A = kwargs.get("A")

        self.m = kwargs.get("m")

        self.V = kwargs.get("v")

        self.a = H/self.m*self.V

        self.F = kwargs.get("F")

    def psi(self,x,t):
        return self.A*(math.sin((x*2*pi)/self.a - self.F*2*pi*t))


def Fg(ambient: ambient,body1: body):
    for body2 in ambient.objects:
        if body1.id != body2.id:
            G = ambient.G
            ab = body2.pos-body1.pos
            r = abs(body1.pos - body2.pos)
            
            if r >= H:
                F_scale = G*body1.m*body2.m/r**2

                F_vector = to_vector(F_scale,ab)

                body2.apply_force("Fg",F_vector*-1)

    return body2

def Fat(ambient: ambient,body1: body):
    Fat = body1.v*(body1.fric/2)*-2
    body1.apply_force("Fat",Fat)
    print(Fat.values)
    return Fat

def Fp(ambient: ambient,body1: body,*args):
    if body1.pos.values[1] > 0:
        body1.apply_force("Fp", vector(0,-body1.m*0.098,0))

        print("fp",body1.resultant_forces['Fp'].values)

    else:
        body1.v.values[1] = 0

    print("y",body1.pos.values[1])


def Tuv(U: vector,p,P,u: vector,n: tensor):
    v = U/abs(U)
    pp = (p+P)
    Uvu = U**(v+u)
    Pn = P*n

    return pp*Uvu + Pn

