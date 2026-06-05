import csv
import os

def kwh_para_reais (empresa):
    grupo_empresa = empresa["grupo"]
    regime = empresa["regime"]
    atividade = empresa["atividade"]

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
    
    if regime == "simples": 
        PIS_COFINS = 0.0
    elif regime == "presumido":
        PIS_COFINS = 0.0365
    elif regime == "real":
        PIS_COFINS = 0.0925
    
    if atividade == "comercio":
        ICMS = 0.18
    elif atividade == "industria":
        ICMS = 0.12

    return kwh, PIS_COFINS, ICMS, TARIFA_BASE, grupo_empresa

def calculo(empresa):
    kwh, PIS_COFINS, ICMS, TARIFA_BASE, grupo_empresa = kwh_para_reais(empresa)
    print(f"R${com_impostos(kwh, TARIFA_BASE, PIS_COFINS, ICMS, grupo_empresa):.2f}")

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

    print("Aparelho cadastrado!")

def visualizar_aparelhos():
    with open ("data/aparelhos.csv", "r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        cabecalho = next(leitor)
        ler = list(leitor)
        if not ler:
            print("Não existem aparelhos cadastrados! Adicione-os.")
        else:
            print("\nAparelhos cadastrados")
        for i, ler in enumerate(ler, start=1):
            print(f"[{i}] ▸ Nome: {ler[0]} ▸ Setor: {ler[1]} ▸ Voltagem: {ler[2]}")


def deletar_aparelho():
    nome_aparelho_deletar = input("\n▸ Nome: ")

    try:
         with open ("data/aparelhos.csv", "r", newline="", encoding="utf-8") as arquivo:
            leitor = csv.reader(arquivo)
            aparelhos = list(leitor)

         novos_aparelhos = []

         for linha in aparelhos:
            if not linha:
                continue 
            if linha[0].lower() == nome_aparelho_deletar.lower():
                print(f"\nAparelho encontrado!\n\n▸ Nome: {linha[0]} ▸ Setor: {linha[1]} ▸ Voltagem: {linha[2]}\n")
                confirmacao = input("Tem certeza que deseja deletar esse aparelho? \n\n[1] Sim / [2] Não: ")

                if confirmacao == "1":
                    print("\nAparelho deletado com sucesso!")

                    index_atual = aparelhos.index(linha)
                    novos_aparelhos.extend(aparelhos[index_atual + 1:])
                    break 
            
            novos_aparelhos.append(linha)
         else: 
             print("Aparelho não encontrado!")
             return
         
         with open("data/aparelhos.csv", "w", newline="", encoding="utf-8") as arquivo:
             escritor = csv.writer(arquivo)
             escritor.writerows(novos_aparelhos)

    except FileNotFoundError:
        print("Arquivo de aparelhos não encontrado.")

            
 


    

def atualizar_aparelho():
    nome_aparelho=input("Digite o nome do aparelho: ")
    setor_aparelho=input("Digite o setor do aparelho: ")
    voltagem_aparelho=input("Digite a voltagem do aparelho: ")
    execucao=0

    with open("data/aparelhos.csv", 'r', newline='', encoding='utf-8') as arquivo, \
         open("data/aparelhos_temp.csv", 'w', newline='', encoding='utf-8') as arquivo_temp:
        
        leitor = csv.reader(arquivo)
        escritor = csv.writer(arquivo_temp)
        
        cabecalho = next(leitor)
        escritor.writerow(cabecalho)

        for i in leitor:
            if not i:
                continue
            if i[0] == nome_aparelho:
                i[1] = setor_aparelho
                i[2] = voltagem_aparelho
                execucao=1
            escritor.writerow(i)
    if execucao==1:
        os.replace("data/aparelhos_temp.csv", "data/aparelhos.csv")
        print("Aparelho atualizado")
    else:
        print("nome não encontrado")
