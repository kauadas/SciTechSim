import periodictable


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
        share_eletrons = 0
        elements = []
        electronegativity = 0
        for type_,i in self.connects:
            if type_ == "=":
                share_eletrons += 4

            elif type_ == "-":
                share_eletrons += 2

            elif type_ == "#":
                share_eletrons += 6
            
            elements.append(i.symbol)

            if i.symbol != self.symbol:
                electronegativity += i.electronegativity
                
        self.formal_charge = self.free_eletrons - ((self.free_eletrons-share_eletrons) + 0.5*share_eletrons)


        self.Nox = self.free_eletrons-self.formal_charge


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

        self.free_eletrons = 1

        self.electronegativity = 2.2

    def calculate_Nox(self):
        pass

# oxigenio
class oxygen(Element):
    def __init__(self):
        super().__init__(
            symbol = "O",
            name ="oxygen",
            N=8,
            free_eletrons=-2
        )

        self.M = 16

        self.period = 2

        self.group = 16

        self.free_eletrons = 6

        self.electronegativity = 3.44

    def calculate_Nox(self):
        self.Nox = 2
        for i in self.connects:
            if i[1].symbol == self.symbol:
                self.Nox = 1

# carbono
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

        self.free_eletrons = 4

        self.electronegativity = 2.55

    def calculate_Nox(self):
        self.Nox = -4

        for i in self.connects:
            if i[1].symbol == "O":
                self.Nox += +2

            elif i[1].symbol == "H":
                self.Nox += -4


#cloro
class chlorine(Element):
    def __init__(self):
        super().__init__(
            symbol = "Cl",
            name ="chlorine",
            N=17,
            Nox=+1
        )

        self.M = 35.5

        self.period = 2

        self.group = 14

        self.free_eletrons = 5

        self.electronegativity = 3.16

    def calculate_Nox(self):

        for i in self.connects:
            if self.electronegativity > i[1].electronegativity:
                self.Nox = i[1].Nox
                i[1].Nox = abs(i[1].Nox)

            else:
                self.Nox = i[1].Nox
                i[1].Nox = abs(i[1].Nox)




class periodicTable:
    def __init__(self):
        self.table = {"H": hidrogen,"O": oxygen,"C": carbon,"Cl": chlorine}

    def add_element(self,symbol: str,element: Element):
        self.table[symbol] = element


    def get_by(self,symbol):
        
        return self.table.get(symbol,None)


#classe que define uma molecula
class molecule:
    def __init__(self,*formule):
        self.atoms = {}

        self.formule = formule

        self.covalent_number = 0
        self.setup()
        self.Nox = 0
        

        self.calculate_nox()


    def setup(self):
        elements = {}
        for n,i in enumerate(self.formule):
            element = periodicTable().get_by(symbol=i[0])

            element = element()

            self.atoms[str(n)] = element

        for n,i in enumerate(self.formule):
            element0 = self.atoms.get(str(n))
            for c in i[1::]:
                type = c[0]
                print(c)
                element1 = self.atoms.get(str(c[1]))
                element0.connect(type,element1)
                


    def get_formule(self):
        chemical_formula = ""
        formule = [i.symbol for i in self.atoms.values()]
        F = []
        for symbol in formule:
            count = formule.count(symbol)
            if symbol not in F:
                if count == 1:
                   chemical_formula += symbol
                else:
                   chemical_formula += symbol + str(count)

                F.append(symbol)


        return chemical_formula


    def calculate_nox(self):
        elements = [i.symbol for i in self.atoms.values()]
        for i in list(self.atoms.values()):
            
            i.calculate_Nox()
            
            
            electronegativity = 0
            uses = []
            for i2 in self.atoms.values():
                if i.symbol != i2.symbol and i2.symbol not in uses:
                    
                    electronegativity += i2.electronegativity

                    uses.append(i2.symbol)

            
            if i.electronegativity > electronegativity:
                i.Nox *= -1

            print(i.name,i.Nox)

            self.Nox += i.Nox

