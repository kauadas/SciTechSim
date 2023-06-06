import math

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
    def __init__(self,infos: dict):
        self.m = infos.get("m", 0)
        self.Q = infos.get("Q", 0)
        self.pos = infos.get("pos", [0, 0, 0])
        self.v = infos.get("v", [0, 0, 0])
        self.a = infos.get("a", [0, 0, 0])

        self.colision = {}


    def upgrade(self):
        self.pos = add_lists(self.pos,self.v)
        self.v = add_lists(self.v,self.a)

def to_vector(i: float,ab: list):
    abs_ab = abs_vector(ab)

    nAB = [x/abs_ab for x in ab]

    Y = [i*x for x in nAB]

    return Y

   