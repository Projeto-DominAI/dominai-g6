amperagem = int(input("Amperagem: ")) # valor captado pela IoT
voltagem = int(input("Voltagem: ")) # valor captado pela IoT
horas_uso = int(input("Horas de uso: ")) # valor captado pela IoT
TARIFA_BASE = 0.77 # constante
bandeira_tarifaria = input("Bandeira tarifária atual: ").lower().strip() # API que pega essa infromação
PIS_COFINS = 0.05 # API que pega essa informação | valor que oscila todo mês
ICMS = 0.205 # API que pega essa informação

def watt (amperagem, voltagem):
    return amperagem * voltagem 

def kwh (amperagem, voltagem, horas_uso):
    return (watt(amperagem, voltagem) / 1000) * horas_uso 

def com_bandeiras (amperagem, voltagem, horas_uso, TARIFA_BASE, bandeira_tarifaria):
    if bandeira_tarifaria == "verde":
        return kwh(amperagem, voltagem, horas_uso) * TARIFA_BASE
    
    elif bandeira_tarifaria == "amarela":
        return (kwh(amperagem, voltagem, horas_uso) * TARIFA_BASE) + kwh(amperagem, voltagem, horas_uso) * 0.01885

    elif bandeira_tarifaria == "vermelha patamar 1":
        return (kwh(amperagem, voltagem, horas_uso) * TARIFA_BASE) + kwh(amperagem, voltagem, horas_uso) * 0.04463 
    
    elif bandeira_tarifaria == "vermelha patamar 2":
        return (kwh(amperagem, voltagem, horas_uso) * TARIFA_BASE) + kwh(amperagem, voltagem, horas_uso) * 0.07877
    
    else:
        print("Digite uma bandeira válida.")

def com_impostos (amperagem, voltagem, horas_uso, TARIFA_BASE, bandeira_tarifaria, PIS_COFINS, ICMS):
    return com_bandeiras(amperagem, voltagem, horas_uso, TARIFA_BASE, bandeira_tarifaria) / (1 - (PIS_COFINS + ICMS))


print(f"R${com_impostos(amperagem, voltagem, horas_uso, TARIFA_BASE, bandeira_tarifaria, PIS_COFINS, ICMS):.2f}")

# Em Recife, a distribuidora é Neoenergia Pernambuco



