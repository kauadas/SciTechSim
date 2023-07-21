from modules import chemical


mol = chemical.molecule(("H",("-",1)),("O",("-",2)),("O",("-",3)),("H"))

print(mol.get_formule())
print(mol.Nox)