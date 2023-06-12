class Element:
    def __init__(self,**kwargs):
        self.symbol = str(kwargs.get("symbol","?"))

        self.name = str(kwargs.get("name",""))

        self.N = float(kwargs.get("N",0))

        self.M = float(kwargs.get("M",0))

        self.is_metal = bool(kwargs.get("is_metal",False))

        self.electronegativity = float(kwargs.get("eletronegativity",3.44))

        self.Nox = int(kwargs.get("Nox",-1))

        self.group = int(kwargs.get("group",1))

        self.period = int(kwargs.get("period",1))

        self.fusion = float(kwargs.get("fusion",0))


C = Element(symbol="C",name="carbon",N=6,M=12.011,Nox=-4,group=14,period=2,fusion=3550)

class molecule:
    def __init__(self,formule: list):
        pass