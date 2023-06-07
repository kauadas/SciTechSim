
import math
import time

#classe pai terminal
class terminal:
    def __init__(self):
        self.v = 0
        self.i = 0
        self.hz = 0
        self.out = []

    def set(self,**kwargs):
        self.v = kwargs.get('v',self.v)
        self.i = kwargs.get('i',self.i)
        self.hz = kwargs.get('hz',self.hz)

# classe pai component
class component:
    def __init__(self,infos: dict):

        self.terminals = {}

        self.r = infos.get("r",10)

        self.time = 1

        self.temp = infos.get('temp',20)

        self.max_temp = infos.get('max_temp',200)

        self.is_break = False

    def get_status(self):
            return {
                "is break?": self.is_break,
                "temp": self.temp,
                "max_temp": self.max_temp,
                "terminals": self.terminals
            }

    def add_connection(self,component,terminal: str):
        pass
        
    def remove_connection(self,component):
        pass
        
    def forward(self):
        pass

    def upgrade(self,i,v,hz):
        pass

