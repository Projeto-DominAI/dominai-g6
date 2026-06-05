import csv
import os
import datetime

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
    id_equipamento = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    nome_equipamento = input("▸ Nome do Equipamento: ")
    setor_equipamento = input("▸ Setor/Localização: ")
    id_sensor = input("▸ ID do Sensor: ")

    tensao_nominal_equipamento = input("▸ Tensão Nominal (V): ")
    corrente_nominal_equipamento = input("▸ Corrente Nominal (A): ")
    horas_previstas_equipamento = input("▸ Horas de Operação Previstas (h/dia): ")

    with open ("data/aparelhos.csv", "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([id_equipamento, nome_equipamento, setor_equipamento, id_sensor,
                           tensao_nominal_equipamento, corrente_nominal_equipamento,
                           horas_previstas_equipamento])

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
            print(f"[{i}]")
            print(f"  ▸ {'ID do Equipamento':<38} {ler[0]}")
            print(f"  ▸ {'Nome do Equipamento':<38} {ler[1]}")
            print(f"  ▸ {'Setor/Localização':<38} {ler[2]}")
            print(f"  ▸ {'ID do Sensor':<38} {ler[3]}")
            print(f"  ▸ {'Tensão Nominal (V)':<38} {ler[4]}")
            print(f"  ▸ {'Corrente Nominal (A)':<38} {ler[5]}")
            print(f"  ▸ {'Horas de Operação Previstas (h/dia)':<38} {ler[6]}")

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
    execucao=0
    nome_aparelho=input("Digite o nome do aparelho: ").strip()
    with open("data/aparelhos.csv", 'r', newline='', encoding='utf-8') as arquivo, \
        open("data/aparelhos_temp.csv", 'w', newline='', encoding='utf-8') as arquivo_temp:
        leitor = csv.reader(arquivo)
        escritor = csv.writer(arquivo_temp)
        cabecalho = next(leitor)
        escritor.writerow(cabecalho)
        for i in leitor:
            if i[1] == nome_aparelho:
                while True:
                    print(f"1-nome:          {i[1]}\n2-setor:         {i[2]}\n3-tensão:        {i[4]}\n4-ID do Sensor: {i[3]}\n5-amperagem:     {i[5]}\n6-horas:         {i[6]}")
                    escolha=int(input("escolha um para editar\n"))
                    if escolha==1:
                        print(f"setor atual: {i[1]}")
                        nome=input("Digite o novo nome do aparelho: ")
                        execucao=2
                        i[1] = nome.strip()
                    elif escolha==2:
                        print(f"setor atual: {i[2]}")
                        setor_aparelho=input("Digite o setor do aparelho: ")
                        execucao=2
                        i[2] = setor_aparelho.strip()
                    elif escolha==3:
                        print(f"voltagem atual: {i[4]}")
                        voltagem_aparelho=input("Digite a voltagem do aparelho: ")
                        execucao=2
                        i[4] = voltagem_aparelho.strip()
                    elif escolha==4:
                        print(f"ID do sensor atual atual: {i[3]}")
                        id_sensor=input("Digite o novo ID do Sensor: ")
                        execucao=2
                        i[4] = id_sensor.strip()
                    elif escolha==5:
                        print(f"amperagem atual: {i[5]}")
                        amperagem_aparelho=input("Digite a amperagem do aparelho: ")
                        execucao=2
                        i[5] = amperagem_aparelho.strip()
                    elif escolha==6:
                        print(f"horas atuais: {i[6]}")
                        horas=input("Digite a quantidade de horas do aparelho: ")
                        execucao=2
                        i[6] = horas.strip()
                    if execucao==2:
                        escolha=int(input("Você deseja editar mais alguma informação?\n[1] Sim\n[2] Não\n"))
                        if escolha==2:
                            break
                    if execucao!=2:
                        print("opção inválida")

            escritor.writerow(i)
    if execucao==2:
        os.replace("data/aparelhos_temp.csv", "data/aparelhos.csv")
        print("Aparelho atualizado")
    if execucao==0:
        print("aparelho não encontrado")
        os.remove("data/aparelhos_temp.csv")
