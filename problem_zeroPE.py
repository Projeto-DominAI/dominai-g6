
vinicial = 1
cont = 0
soma = 0

for cont in range(0, 10, 1):
    potencia = (vinicial * cont)**2 
    if potencia % 2 != 0:
        soma += potencia
print(soma)
