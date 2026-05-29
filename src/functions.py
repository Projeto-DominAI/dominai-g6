import csv

def kwh_para_reais ():
    grupo_empresa = input("Digite o Tipo da empresa A ou B: ").lower().strip()
    if grupo_empresa == "b":
        amperagem = float(input("\nAmperagem: "))

        voltagem = float(input("Voltagem: "))

        horas_uso = float(input("Horas de uso: "))
        
        watt = amperagem * voltagem

        kwh = (watt/1000) * horas_uso
        
        TARIFA_BASE = 0.79
    elif grupo_empresa == "a":
        kwh_fora =  float(input("Consumo fora da ponta (kwh/mês): "))
        kwh_ponta = float(input("Consumo na ponta (kwh/mês): "))
        demanda_contratada = float (input("Demanda contratada de (kW): "))
        
        TARIFA_FORA_PONTA = 0.61
        TARIFA_PONTA = 2.50
        TARIFA_DEMANDA = 40

        custo_fora = kwh_fora * TARIFA_FORA_PONTA
        custo_ponta = kwh_ponta * TARIFA_PONTA
        custo_demanda = demanda_contratada * TARIFA_DEMANDA

        TARIFA_BASE = custo_fora + custo_ponta + custo_demanda
        kwh = kwh_fora + kwh_ponta

    regime = input("Regime da empresa (simples/presumido/real): ").lower().strip() 
    while True:
            if regime == "simples":
                PIS_COFINS = 0.0
                break
            elif regime == "presumido":
                PIS_COFINS = 0.0365
                break
            elif regime == "real":
                PIS_COFINS = 0.0925
                break
            else:
                print("Digite uma opção valida.")
                continue

    atividade = input("Digite a atividade (comercio ou industria): ").lower().strip()
    while True:
        if atividade == "comercio":
            ICMS = 0.18
            break
        elif atividade == "industria":
            ICMS = 0.12
            break
        else:
            print("Digite uma opção valida.")
            continue

    return kwh, PIS_COFINS, ICMS, TARIFA_BASE, grupo_empresa
    


def com_bandeiras (kwh, TARIFA_BASE, grupo_empresa):
    bandeira_tarifaria = input("Digite o tipo da bandeira (verde / amarela / vermelha / vermelha2) ").lower().strip()
    while True:
        if grupo_empresa == "b":
            if bandeira_tarifaria == "verde":
                return kwh * TARIFA_BASE
            elif bandeira_tarifaria == "amarela":
                return (kwh * TARIFA_BASE) + kwh * 0.01885
            elif bandeira_tarifaria == "vermelha":
                return (kwh * TARIFA_BASE) + kwh * 0.04463
            elif bandeira_tarifaria == "vermelha2":
                return (kwh * TARIFA_BASE) + kwh * 0.07877
            else:
                print("Bandeira inválida.")
                bandeira_tarifaria = input("Bandeira: ").lower().strip()

        elif grupo_empresa == "a":
            if bandeira_tarifaria == "verde":
                return TARIFA_BASE
            elif bandeira_tarifaria == "amarela":
                return TARIFA_BASE + kwh * 0.01885
            elif bandeira_tarifaria == "vermelha":
                return TARIFA_BASE + kwh * 0.04463
            elif bandeira_tarifaria == "vermelha2":
                return TARIFA_BASE + kwh * 0.07877
        else:
            break    

def com_impostos(kwh, TARIFA_BASE, PIS_COFINS, ICMS, grupo_empresa):
    return com_bandeiras(kwh, TARIFA_BASE, grupo_empresa) / (1 - (PIS_COFINS + ICMS))

def calcular():
    kwh, PIS_COFINS, ICMS, TARIFA_BASE, grupo_empresa = kwh_para_reais()
    print(f"R${com_impostos(kwh, TARIFA_BASE, PIS_COFINS, ICMS, grupo_empresa):.2f}")

def cadastrar_aparelho ():
    nome_aparelho = input("▸ Nome: ")
    setor_aparelho = input("▸ Setor: ")
    voltagem_aparelho = input("▸ Voltagem: ")

    with open ("data/aparelhos.csv", "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([nome_aparelho, setor_aparelho, voltagem_aparelho])

def visualizar_aparelhos():
    with open ("aparelhos.csv", "r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        ler = list(leitor)
        if not ler:
            print("Não existem aparelhos cadastrados! Adicione-os.")
        else:
            print("\nAparelhos que cadastrados")
        for i, ler in enumerate(ler, start=1):
            print(f"{i} - Nome: {ler[0]} - Setor: {ler[1]} - Voltagem: {ler[2]}")
