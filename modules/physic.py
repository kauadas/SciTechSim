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
 

class vector:
    def __init__(self,*args):
        self.values = args

    def __add__(self,other):
        if isinstance(other,vector):
            return vector(*[x + y for x,y in zip(self.values,other.values)])

        elif isinstance(other,int):
            return vector(*[x + other for x in self.values])

    def __sub__(self,other):
        if isinstance(other,vector):
            return vector(*[x - y for x,y in zip(self.values,other.values)])

        elif isinstance(other,int):
            return vector(*[x - other for x in self.values])


    def __mul__(self,other):
        if isinstance(other,vector):
            return vector(*[x * y for x,y in zip(self.values,other.values)])

        else:
            return vector(*[x * other for x in self.values])

    def __truediv__(self,other):
        if isinstance(other,vector):
            return vector(*[x / y for x,y in zip(self.values,other.values)])

        else:
            return vector(*[x / other for x in self.values])

    def __pow__(self,other):
        if isinstance(other,vector):
            return vector(*[x ** y for x,y in zip(self.values,other.values)])

        elif isinstance(other,int):
            return vector(*[x ** other for x in self.values])


    def __iadd__(self, other):
            if isinstance(other, vector):
                self.values = [x + y for x,y in zip(self.values,other.values)]
            else:
                self.values = [x + other for x in self.values]

            return self

    def __isub__(self, other):
            if isinstance(other, vector):
                self.values = [x - y for x,y in zip(self.values,other.values)]
            else:
                self.values = [x - other for x in self.values]

            return self


    def sqrt(self):
        return vector(*[math.sqrt(x) for x in self.values])

    def __abs__(self):
        y = 0
        for i in self.values:
            y += i**2

        return math.sqrt(y)


#classe pai body representa corpos físicos
class body:
    def __init__(self,**kwargs):
        self.m = kwargs.get("m", 0)
        self.Q = kwargs.get("Q", 0)
        self.resultant_forces = {}
        self.pos = vector(*kwargs.get("pos", [0, 0, 0]))
        self.v = vector(*kwargs.get("v", [0, 0, 0]))
        self.a = vector(*kwargs.get("a", [0, 0, 0]))

        self.angle = vector(*kwargs.get("angle", [0, 0, 0]))
        self.aV = vector(*kwargs.get("angular_velocity", [0, 0, 0]))
        self.aA = vector(*kwargs.get("angular_aceleration", [0, 0, 0]))
        

        self.image = {}


    def upgrade(self):
        self.a = sum(list(self.resultant_forces.values),start=vector(*[0 for i in self.body.pos]))/self.m
        self.pos = self.pos + self.v
        self.v = self.v + self.a
        self.angle = self.angle + self.aV
        self.aV = add_lists(self.aV,self.aA)

    def is_collide(self,obj2):
        for key,value in self.image.items():
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
        self.objects = []
        self.universal_forces = []
        self.w,self.h = kwargs.get("size")

        self.G = kwargs.get("G",G)
        self.K = kwargs.get("K",K)
        self.time = kwargs.get("time",1)

    def upgrade(self):
        for obj in self.objects:
            obj.upgrade()

        for force,i,obj in zip(self.universal_forces,enumarate(self.objects)):
            
            if len(self.objects)-1 >= i+1:
                obj2 = self.objects(i+1)
                force(self.ambient,obj,obj2)

        

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



def navier_stocks(gradient: list,V: list,p,Fbody: list,u):
    Ap = [i*p*-1 for i in gradient]

    uA2 = [u*(i**2) for i in gradient]

    uA2v = [i*i2 for i,i2 in zip(uA2,V)]

    p1 = add_lists(Ap, uA2v)

    return add_lists([p*i for i in Fbody],p1)


class Wave_Particle:
    def __init__(self,**kwargs):
        self.A = kwargs.get("A")

        self.m = kwargs.get("m")

        self.V = kwargs.get("v")

        self.a = H/self.m*self.V

        self.F = kwargs.get("F")

    def psi(self,x,t):
        return self.A*(math.sin((x*2*pi)/self.a - self.F*2*pi*t))


def Fg(ambient: ambient,body1: body,body2: body):
    G = ambient.G
    ab = body2.pos-body1.pos
    r = abs(body1.pos - body2.pos)
    
    F_scale = G*body1.m*body2.m/r**2

    if F_scale/body1.m < C:
        F_vector = to_vector(F_scale,ab)

        body1.resultant_forces["Fg"] = F_vector
        body2.resultant_forces["Fg"] = F_vector*-1

        return F_vector

def Fp(ambient: ambient,body1: body,*args):
    body1.resultant_forces["Fp"] = vector(0,body1.m*ambient.G,0)