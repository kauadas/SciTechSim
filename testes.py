from modules import chemical


mol = chemical.molecule(["O","=","C","=","O"]).atoms.values()

mol_str = ""
in_mol = []
for i in mol:
    
    for s,c in i.connects:
        if not i in in_mol:
            print(s)
            mol_str += i.symbol + s + c.symbol
            in_mol.append(c)

        elif i in in_mol:
            print(s)
            mol_str += s + c.symbol

        elif c in in_mol:
            mol_str += i.symbol + s

print(mol_str)