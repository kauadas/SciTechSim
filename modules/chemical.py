
#classe pai de todos os elementos
class Element:
    def __init__(self,**kwargs):
        self.symbol = str(kwargs.get("symbol","?"))

        self.name = str(kwargs.get("name",""))

        self.N = float(kwargs.get("N",0))

        self.M = float(kwargs.get("M",0))

        self.is_metal = bool(kwargs.get("is_metal",False))

        self.electronegativity = float(kwargs.get("eletronegativity",2.2))

        self.group = int(kwargs.get("group",1))

        self.period = int(kwargs.get("period",1))

        self.fusion = float(kwargs.get("fusion",0))

# tabela periodica


# classe do hidrogenio
class hidrogen(Element):
    def __init__(self):
        super().__init__(
            symbol = "H",
            name ="hidrogen",
            N=1
        )

        self.M = 1

        self.period = 1

        self.group = 0
        
class oxygen(Element):
    def __init__(self):
        super().__init__(
            symbol = "O",
            name ="oxygen",
            N=8
        )

        self.M = 16

        self.period = 2

        self.group = 16
        

class periodicTable:
    def __init__(self):
        self.table = {"H": hidrogen,
                     "O": oxygen}

    def add_element(self,symbol: str,element: Element):
        self.table[symbol] = element


    def get_by(self,symbol):
        
        return self.table.get(symbol,None)


#classe que define uma molecula
class molecule:
    def __init__(self,formule: list):
        self.formule = [(periodicTable().get_by(symbol=E)(),E_Nox) for E,E_Nox in formule]
        self.C = 0
        
        for i,Nox in self.formule:
           self.C += Nox

        self.ion = "N"

        if self.C > 0:
            self.ion = "+"

        if self.C < 0:
            self.ion = "-"

        self.connect_atoms()
    def get_formule(self):
        f = {}
        for i, Nox in self.formule:
            if i.symbol in f:
                f[i.symbol] += 1

            else:
                f[i.symbol] = 1

        formule = ""
        for i,x in f.items():
            if x == 1:
                x = ""

            formule += f"{i}{x}"


        return formule

    def connect_atoms(self):
        for i in range(len(self.formule)):
            atom = self.formule[i][0]
            atom.neighbors = []  # Limpa as conexões existentes

            if i > 0:
                previous_atom = self.formule[i - 1]
                atom.neighbors.append(previous_atom)

            if i < len(self.formule) - 1:
                next_atom = self.formule[i + 1]
                atom.neighbors.append(next_atom)

    def __add__(self,other):
        F1 = [(i.symbol,Nox) for i,Nox in self.formule]
        F2 = [(i.symbol,Nox) for i,Nox in other.formule]
        if self.C > 0:
           x = F1 + F2

        else:
            x = F2 + F1

        x = molecule(x)
        print(f"{self.get_formule()} + {other.get_formule()} -> {x.get_formule()}")

        return x

    def __mul__(self,other):
        x = []
        F1 = [(i.symbol,Nox) for i,Nox in self.formule]

        
        
        for i in range(other):
            x += F1
        return molecule(x)

    def __truediv__(self,other):
        r = []
        F1 = [(i.symbol,Nox) for i,Nox in self.formule]
        for i in F1:
            x = (i,F1.count(i))
            if not str(x) in str(r):
                r.append(x)

        M = []
        for i,x in r:
            for v in range(int(x/2)):
                M.append(i)
        x = molecule(M)

        print(f"{self.get_formule()} / {other} -> {x.get_formule()}")

        return x
            
            
            




def decomposition_reaction(mol):
    elements = mol.formule
    result = []

    for element in elements:
        for i in range(len(result)):
            if result[i][0]().symbol == element().symbol:
                result[i].append(element)
                break
        else:
            result.append([element])

    return [molecule(m) for m in result]
