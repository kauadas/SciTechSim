from modules.chemical import *

H2 = molecule([("H",1),("H",1)])

O2 = molecule([("O",-2),("O",-2)])

result = H2 + O2/2

print("formula final: ",result.get_formule())

print("Nox da molecula: ",result.C)