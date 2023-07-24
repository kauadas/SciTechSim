import math
from modules import physic 

def calc(gradient: list,V: list,p,Fbody: list,u):
    Ap = [i*p for i in gradient]

    nAp = [i*-1 for i in Ap]

    uA2 = [u*(i**2) for i in gradient]

    uA2v = [i*i2 for i,i2 in zip(uA2,V)]

    p1 = physic.add_lists(nAp, uA2v)

    return physic.add_lists([p*i for i in Fbody],p1)


gradient = [2,3,4]

V = [15,0,4]


Fbody = [160,0,5]

p = physic.abs_vector(Fbody)/28.26

u = 1.0020/1000

n1 = calc(gradient,V,p,Fbody,u)

print(n1)