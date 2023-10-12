import math

class vector:
    def __init__(self,*args):
        self.values = list(args)

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
            
    def __getitem__(self, item):
         return self.values[item]

    def sqrt(self):
        return vector(*[math.sqrt(x) for x in self.values])

    def __abs__(self):
        y = 0
        for i in self.values:
            y += i**2

        return math.sqrt(y)

class tensor:
    def __init___(self,*args):
        self.values = args

def somatory(u: int, n: int,callback):
    values = [callback(u,n)]

    return sum(values)


def circle_collide(R1: float, pos1: vector,R2: float,pos2: vector):
    D = abs(pos1 - pos2)

    return R1+R2 >= D



def rect_collide(pos1: vector, size1: vector,pos2: vector, size2: vector):
    w,h,p = size1/2+(size2/2)

    Dw,Dh,Dp = pos2-pos1

    return abs(Dw) <= w and abs(Dh) <= h and abs(Dp) <= p
    

    


