
import math
import time

class component():
    def __init__(self,infos: dict):

        self.connections = []

        self.i = 0

        self.v = 0

        self.r = infos.get("r",10)
        
        self.terminal = 1

        self.time = 1

        self.hz = 0

        self.temp = infos.get('temp',20)

        self.max_temp = infos.get('max_temp',200)

        self.break_ = False

    def add_connection(self,component,terminal: str):
        if terminal not in ["+","-"]:
            print("terminal error")

        if terminal == "-":
            component.terminal = -1

        self.connections.append(component)
        
    def remove_connection(self,component):
        self.connections.remove(component)
        
    def forward(self):
        for i in self.connections:
            i.upgrade(i=self.i,v=self.v,hz=self.hz)

    def upgrade(self,i,v,hz):
        pass

class resistor(component):
    def __init__(self, infos: dict):
        super().__init__(infos)

    def upgrade(self,i,v,hz):

        V = (i)*self.r

        Ni = (v)/self.r
        
        print(Ni,V)
        self.i = Ni

        self.v = V

        self.hz = hz

        

        self.forward()

class capacitor(component):
    def __init__(self, infos: dict):
        super().__init__(infos)
        self.C = infos.get('c',10)
        

    def upgrade(self, i,v,hz):
        if hz == 0:
            dV_V = ((v-self.v) / self.time)
        else:
            Fa = 2*3.14*hz
            dV_V = (-Fa * math.sin(Fa))

        I = self.C*dV_V*self.terminal

        self.i = I

        print(self.i)

        self.v = v*self.terminal

        self.forward()


class battery(component):
    def __init__(self, infos: dict):
        super().__init__(infos)
        self.I = infos.get('max_i',1200)
        self.v = infos.get('v',12) 
        self.i = infos.get("i",2) 
        

    def upgrade(self):
        if self.I > self.i:
            self.I -= self.I

            
            self.forward()

class source(component):
    def __init__(self, infos: dict):
        super().__init__(infos)
        
        self.v = infos.get('v',12) 
        self.i = infos.get("i",2) 
        self.hz = infos.get("hz",1)

        if infos['type'] not in ["CC","CA"]:
            print("tipo de corrente invalido arrombado")
            return
        
        if infos['type'] == "CC":
            self.multiple = 1
            self.hz = 0

        else:
            self.multiple = -1

    def upgrade(self):
        self.i *= self.multiple
        self.v *= self.multiple

        self.forward()

B1 = source({"type": "CA"})

C1 = capacitor({"c": 10})

B1.add_connection(C1,"+")


for i in range(4):
    B1.upgrade()
    print(C1.i,C1.v)
    time.sleep(1)