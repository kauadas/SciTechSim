
#classe pai de todos os elementos
class Element:
    def __init__(self,**kwargs):
        self.symbol = str(kwargs.get("symbol","?"))

        self.name = str(kwargs.get("name",""))

        self.N = float(kwargs.get("N",0))

        self.M = float(kwargs.get("M",0))

        self.is_metal = bool(kwargs.get("is_metal",False))

        self.electronegativity = float(kwargs.get("eletronegativity",2.2))

        self.Nox = int(kwargs.get("Nox",-1))

        self.group = int(kwargs.get("group",1))

        self.period = int(kwargs.get("period",1))

        self.fusion = float(kwargs.get("fusion",0))

# tabela periodica
class periodicTable:
    def __init__(self):
        self.table = {}

    def add_element(self,symbol: str,element: Element):
        self.table[symbol] = element


    def get_by(symbol: str):
        return self.table.get(symbol,None)


# classe do hidrogenio
class hidrogen(Element):
    def __init__(self):
        super().__init__(
            symbol = "H",
            name ="hidrogen",
            N=1
        )

        self.M = 1

        self.Nox = +1

        self.period = 1

        self.group = 0
        
        

#classe que define uma molecula
class molecule:
    def __init__(self,formule: list):
        self.formula = [i() for i in formule]
        self.connect_atoms()

    def connect_atoms(self):
        for i in range(len(self.formula)):
            atom = self.formula[i]
            atom.neighbors = []  # Limpa as conexões existentes

            if i > 0:
                previous_atom = self.formula[i - 1]
                atom.neighbors.append(previous_atom)

            if i < len(self.formula) - 1:
                next_atom = self.formula[i + 1]
                atom.neighbors.append(next_atom)

Pt = periodicTable()
H2 = molecule([hidrogen,hidrogen])

print(H2.formula[0].neighbors)