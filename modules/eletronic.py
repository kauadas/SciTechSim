
import math
import time

#classe pai terminal
class terminal:
    def __init__(self):
        self.v = 0
        self.i = 0
        self.hz = 0
        self.out = {}

    def set(self,**kwargs):
        self.v = kwargs.get('v',self.v)
        self.i = kwargs.get('i',self.i)
        self.hz = kwargs.get('hz',self.hz)

    def clear(self):
        self.v = 0
        self.i = 0
        self.hz = 0

# classe pai component
class component:
    def __init__(self,**kwargs):

        self.name = kwargs.get("name")

        self.terminals = {}

        self.r = kwargs.get("r",10)

        self.time = 1

        self.temp = kwargs.get('temp',20)

        self.max_temp = kwargs.get('max_temp',200)

        self.is_break = False

    def get_status(self):
            return {
                "is break?": self.is_break,
                "temp": self.temp,
                "max_temp": self.max_temp,
                "terminals": self.terminals
            }

    def add_connection(self,component,terminal1: str,terminal2: str):
        self.terminals[terminal1].outs[component.name] = [component,terminal2]
        
    def remove_connection(self,component):
        self.terminals[terminal1].outs.pop(component.name)
        
    def forward(self):
        for k,v in self.terminals.items():
            for i,t2 in v.out.values():
                i.set(v=t.v,i=t.i,hz=t.hz)

    def upgrade(self):
        pass


class source(component):
    def __init__(self, kwargs):
        super().__init__(kwargs)

        self.terminals = {"+": terminal(),
                          "-": terminal()}

        self.V = kwargs.get('voltage',12)

        self.i = kwargs.get('amparage',2)

        self.hz = kwargs.get('frequency',1)


    def upgrade(self):
        pass
