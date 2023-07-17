
#classe pai de todos os elementos
class Element:
    def __init__(self,**kwargs):
        self.symbol = str(kwargs.get("symbol","?"))

        self.name = str(kwargs.get("name",""))

        self.N = float(kwargs.get("N",0))

        self.M = float(kwargs.get("M",0))

        self.Nox = float(kwargs.get("Nox",+1))

        self.is_metal = bool(kwargs.get("is_metal",False))

        self.electronegativity = float(kwargs.get("eletronegativity",2.2))

        self.group = int(kwargs.get("group",1))

        self.period = int(kwargs.get("period",1))

        self.fusion = float(kwargs.get("fusion",0))

        self.connects = []


    def connect(self,_type: str,other):
        self.connects.append((_type,other))
        other.connects.append((_type,self))


    def calculate_Nox(self):
        pass
                

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

        self.Nox = 1

        self.electronegativity = 2.2

    def calculate_Nox(self):
        for _type,other in self.connects:
            if other.electronegativity < self.electronegativity:
                self.Nox = -1

        
class oxygen(Element):
    def __init__(self):
        super().__init__(
            symbol = "O",
            name ="oxygen",
            N=8,
            Nox=-2
        )

        self.M = 16

        self.period = 2

        self.group = 16

        self.Nox = -2

        self.electronegativity = 3.44

    def calculate_Nox(self):
        for _type,other in self.connects:
            if other.electronegativity == self.electronegativity:
                self.Nox = -1

            if other.electronegativity > self.electronegativity:
                self.Nox *= -1


        
class carbon(Element):
    def __init__(self):
        super().__init__(
            symbol = "C",
            name ="carbon",
            N=6,
            Nox=+2
        )

        self.M = 12

        self.period = 2

        self.group = 14

        self.Nox = 4

        self.electronegativity = 2.55

        
class periodicTable:
    def __init__(self):
        self.table = {"H": hidrogen,"O": oxygen,"C": carbon}

    def add_element(self,symbol: str,element: Element):
        self.table[symbol] = element


    def get_by(self,symbol):
        
        return self.table.get(symbol,None)


#classe que define uma molecula
class molecule:
    def __init__(self,*formule):
        self.atoms = {}

        self.formule = formule

        self.setup()
        self.Nox = 0

        self.calculate_nox()


    def setup(self):
        elements = {}
        for n,i in enumerate(self.formule):
            element = periodicTable().get_by(symbol=i)
            if element:
                element = element()

                self.atoms[str(int(n/2))] = element

        for n,i in enumerate(self.formule):
            if not periodicTable().get_by(symbol=i):
                element0 = self.atoms[str(int((n-1)/2))]
                element1 = self.atoms[str(int((n+1)/2))]
                element0.connect(i,element1)


    def get_formule(self):
        chemical_formula = ""
        formule = [i.symbol for i in self.atoms.values()]

        F = []
        for symbol in formule:
            count = sum(1 for s in self.formule if s == symbol)
            if symbol not in F:
                if count == 1:
                   chemical_formula += symbol
                else:
                   chemical_formula += symbol + str(count)

                F.append(symbol)


        return chemical_formula


    def calculate_nox(self):
        for i in self.atoms.values():
            
            i.calculate_Nox()

            self.Nox += i.Nox