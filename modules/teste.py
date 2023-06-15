pi = 3.14159265358979323846
def fact(x):
    y = 1
    for i in range(1,x+1):
        y *= i

    return y

def cos(x):
    x = (x / 360) * 2 * pi
    c = 1
    y = 2
    s = 1
    
    for i in range(1,10+1):
        s *= -1
        c += s*((x**(y*i))/fact(y*i))
        


    return c

print(cos(46))