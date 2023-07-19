
import math
import time
 
class current:
    def __init__(self,source):
        self.source = fonte
        self.map = [[self.source]]

    def run(self):
        self.source.upgrade()

#classe que representa um terminal de um componente
class terminal:
    def __init__(self,polarity: str = "+"):
        if polarity not in ["+","-"]:
            raise ValueError("Invalid polarity. Valid polarities are '+' and '-'.")

        self.v = 0
        self.i = 0
        self.hz = 0

        self.out = {}
        if polarity == "+":
            self.polarity = 1

        else:
            self.polarity = -1

 
            

    def set(self,**kwargs):

        self.v = kwargs.get('v',self.v)*self.polarity

        self.i = kwargs.get('i',self.i)*self.polarity

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

        self.Dc = kwargs.get("specific_temp",20.92)/4.184

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
        if self.callback:
            self.callback()

        for k,v in self.terminals.items():
            for i,t2 in v.out.values():
                t = i.get_terminal(t2)
                t_ = [t.v,t.i,t.hz]
                t.set(v=v.v,i=v.i,hz=v.hz)

                if t_ != [t.v,t.i,t.hz]:
                    i.upgrade()
                
                
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
            if i.i > 0:
                Q = (i.i**2)*self.r*self.time
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
        self.get_terminal("+").set(v=self.V,i=self.I,hz=self.Hz)
        self.get_terminal("-").set(v=self.V,i=self.I,hz=self.Hz)

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

            self.porcent = [i/self.volts for i in self.color]
            self.zero = 116/255
            self.light_color = self.off_color


        def upgrade(self):
            Tp = self.get_terminal("+")
            Tn = self.get_terminal("-")


            W = (Tp.v*Tp.i)
            
            if W <= self.watts:
                if Tp.v > 0:
                    Tn.set(v=Tp.v,i=Tp.i,hz=Tp.hz)

                if Tp.v > 0:
                    self.light_color = [i*Tp.v for i in self.porcent]

                else:
                    self.light_color = self.off_color

                self.forward()

            else:
                self.is_break = True

                

                

            


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
        

        self.V = T1.v-T2.v

        self.i = T1.i

        self.hz = T1.hz

        if self.i > 0:
            self.R = self.V/self.i

        else:
            self.R = 0

        self.forward()

        T1.set(v=0,i=0,hz=0)
        

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
            if self.get_terminal("1").v > 0:
                t1 = self.get_terminal("1")
                t2 = self.get_terminal("2")

            if t1.v > 0:
                I = t1.v/self.r
                t2.set(v=t1.v,i=I,hz=t1.hz)
                print(I)

            self.forward()

