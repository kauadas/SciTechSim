
import math
import time

#classe que representa um terminal de um componente

class terminal:
    def __init__(self,polarity: str = "+"):
        if polarity not in ["+","-"]:
            raise ValueError("Invalid polarity. Valid polarities are '+' and '-'.")

        self.out_v = 0
        self.in_v = 0
        self.in_I = 0
        self.out_I = 0
        self.hz = 0

        self.out = {}
        if polarity == "+":
            self.polarity = 1

        else:
            self.polarity = -1

 
            

    def set(self,**kwargs):

        self.in_v = kwargs.get('in_v',self.in_v)*self.polarity

        self.in_I = kwargs.get('in_I',self.in_I)*self.polarity

        self.out_v = kwargs.get('out_v',self.out_v)*self.polarity

        self.out_I = kwargs.get('out_I',self.out_I)*self.polarity


        self.hz = kwargs.get("hz",self.hz)

    def clear(self):
        self.v = 0
        self.i = 0
        self.hz = 0

        

# classe pai de todos os componentes
class component:
    def __init__(self,**kwargs):

        self.name = kwargs.get("name")

        self.terminals = {}

        self.r = kwargs.get("r",172/10000)

        self.is_source = False

        self.time = 1
        
        self.callback = None

        self.Dc = kwargs.get("specific_temp",1)*4.186

        self.ambient_temp = kwargs.get("ambient_temp",20)

        self.temp = kwargs.get('temp',20)

        self.max_temp = kwargs.get('max_temp',200)

        self.is_break = False

        self.callback = None

    def get_status(self):
            return {
                "is break?": self.is_break,
                "temp": self.temp,
                "max_temp": self.max_temp,
                "terminals": self.terminals
            }

    def add_connection(self,component,terminal1: str,terminal2: str):
        self.terminals[terminal1].out[component.name] = [component,terminal2]
        component.terminals[terminal2].out[self.name] = [self,terminal1]
        
    def remove_connection(self,component,terminal1: str,terminal2: str):
        self.terminals[terminal1].out.pop(component.name)
        component.terminals[terminal2].out.pop(self.name)

    def forward(self):
        

        for k,v in self.terminals.items():
                for i,t2 in v.out.values():
                    t = i.get_terminal(t2)
                    t_ = [t.in_v,t.in_I,t.hz]
                    t.set(in_v=v.out_v,in_I=v.out_I,hz=v.hz)
                    t2 = [t.in_v,t.in_I,t.hz]

                    print(i.name)

                        


        if self.callback:
            self.callback()
                
                
    def reset(self):
        for i in self.terminals.values():
            i.set(v=0,i=0,hz=0)
        
        self.is_break = False
                

    def get_terminal(self,terminal_: str):
        if terminal_ in self.terminals:
            return self.terminals.get(terminal_)

        else:
            raise KeyError(f"terminal {terminal_} don't found.")
            

    def upgrade_status(self):
        for i in self.terminals.values():
            if i.in_I > 0:
                Q = (i.in_I**2)*self.r*self.time
                self.temp += Q/self.Dc

        if self.temp != self.ambient_temp:
            self.temp += (self.ambient_temp - self.temp)/self.Dc

        if self.temp > self.max_temp:
            self.is_break = True

    def upgrade(self):
        pass


class source(component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.terminals = {"+": terminal(polarity="+"),
                          "-": terminal(polarity="-")}

        self.type = "source"
        self.is_source = True

        self.V = kwargs.get('voltage',12)
        self.Dv = self.V
        self.I = kwargs.get('amparage',2)
        self.Di = self.I
        self.Hz = kwargs.get('frequency',1)
        self.Dhz = self.Hz

        

    def upgrade(self):
        self.get_terminal("+").set(out_v=self.V,out_I=self.I,hz=self.Hz)
        self.get_terminal("-").set(out_v=self.V,out_I=self.I,hz=self.Hz)
        self.forward()


class Led(component):
        def __init__(self,**kwargs):
            super().__init__(**kwargs)
            
            self.terminals = {"+": terminal(polarity="+"),
                            "-": terminal(polarity="-")}

            self.type = "led"

            self.color = kwargs.get("light_color",[255,0,0])+[255]

            self.off_color = [i/2 for i in self.color]

            self.volts = kwargs.get("voltage",5)

            self.current = kwargs.get("current",0.02)
            
            self.watts = self.volts*self.current

            self.porcent = [i/self.watts for i in self.color]
            self.zero = 116/255
            self.light_color = self.off_color


        def upgrade(self):
            Tp = self.get_terminal("+")
            Tn = self.get_terminal("-")


            W = (Tp.in_v*Tp.in_I)
            
            if not self.is_break:
                if W <= self.watts:
                    if Tp.in_v > 0:
                        Tn.set(out_v=Tp.in_v,out_I=Tp.in_I,hz=Tp.hz)
                        self.light_color = [i*Tp.in_v*Tp.in_I for i in self.porcent]

                    else:
                        self.light_color = self.off_color

                    self.forward()

                else:
                    self.is_break = True

        def set_color(self,color: list):
            self.color = color+[255]
            self.off_color = [i/2 for i in self.color]
                

                

            


class Multimeter(component):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.terminals = {"+": terminal(polarity="+"),
                          "-": terminal(polarity="-")}

        

        self.type = "multimeter"

        self.V = 0

        self.i = 0

        self.hz = 0

        self.R = 0

    def upgrade(self):
        T1 = self.get_terminal("+")
        T2 = self.get_terminal("-")
        

        self.V = T1.in_v - T2.in_v

        self.i = T1.in_I - T2.in_I

        self.hz = T1.hz - T2.hz

        if self.i > 0:
            self.R = self.V/self.i

        else:
            self.R = 0

        T2.set(out_v=T1.in_v,out_I=T1.in_I,hz=self.hz)

        self.forward()

        

class  wire(component):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


        self.terminals = {"+": terminal(polarity="+"),
                          "-": terminal(polarity="-")}

        
    def upgrade(self):
        self.upgrade_status()
        t1 = self.get_terminal("+")
        self.get_terminal('-').set(v=t1.v,i=t1.i,hz=t1.Hz)
        
        self.forward()

class Resistor(component):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.type = "resistor"
        
        self.r = kwargs.get("r",10)
        self.terminals = {"1": terminal(polarity="+"),
                          "2": terminal(polarity="+")}

        
    def upgrade(self):
        
        if not self.is_break:
            self.upgrade_status()

            t1 = self.get_terminal("2")
            t2 = self.get_terminal("1")
            if self.get_terminal("1").in_v > 0:
                t1 = self.get_terminal("1")
                t2 = self.get_terminal("2")

            
            I = t1.in_v/self.r
            t2.set(out_v=t1.in_v,out_I=I,hz=t1.hz)
            print(I)

            self.forward()

        else:
            print("break")




class Pic(component):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.code = ""

    def upgrade(self):
        eval("from modules import pic",self.code)
        self.forward()


class picCompiler:
    def __init__(self,pic: Pic,code: str):
        self.low = 0
        self.high = 5
        self.pic = pic
        self.code = code

    def digital_write(self,port: int,value: int):
        self.pic.get_terminal(port).set(v=value)

class Capacitor(component):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.terminals = {"+": terminal(polarity="+"),
                          "-": terminal(polarity="-")}

        self.c = kwargs.get("C",10)
        self.old_i = 0
        self.C_i = 0

    def upgrade(self):
        tp = self.get_terminal("+")
        tn = self.get_terminal("-")

        if not self.is_break:
            if self.old_i != 0 and tp.in_I != self.old_i:
                tn.set(out_I=self.C_i,out_v=tp.in_v)

            elif self.C_i + tp.in_I > self.c*tp.in_v:
                self.is_break = True

            else:
                self.old_i = tp.in_I

                self.C_i += tp.in_I

            



