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
    nome_equipamento = input("▸ Nome do Equipamento: ").strip()
    setor_equipamento = input("▸ Setor/Localização: ").strip()
    id_sensor = input("▸ ID do Sensor: ").strip().upper()

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
            cabecalho = next(leitor)
            aparelhos = list(leitor)

         aparelhos_encontrados = []

         for linha in aparelhos:
            if not linha:
                continue
            if linha[1].strip().lower().replace("-", " ") == nome_aparelho_deletar.strip().lower().replace("-", " "):
                aparelhos_encontrados.append(linha)

         if len(aparelhos_encontrados) == 0:
             print("Aparelho não encontrado!")
             return

         encontrou = 0
         linha_deletar = []

         if len(aparelhos_encontrados) > 1:
             print(f"\nForam encontrados {len(aparelhos_encontrados)} aparelhos com esse nome:\n")
             i = 1
             for linha in aparelhos_encontrados:
                 print(f"  [{i}] ID: {linha[0]}  ▸ Setor: {linha[2]}  ▸ Tensão: {linha[4]}V")
                 i += 1

             while encontrou == 0:
                 escolha = input("\n▸ Digite o número do aparelho que deseja deletar: ")
                 if escolha.isdigit() and 1 <= int(escolha) <= len(aparelhos_encontrados):
                     linha_deletar = aparelhos_encontrados[int(escolha) - 1]
                     encontrou = 1
                 else:
                     print("Opção inválida. Tente novamente.")
         else:
             linha_deletar = aparelhos_encontrados[0]

         print(f"\nAparelho encontrado!\n\n▸ Nome: {linha_deletar[1]} ▸ Setor: {linha_deletar[2]} ▸ Tensão: {linha_deletar[4]}\n")
         confirmacao = input("Tem certeza que deseja deletar esse aparelho? \n\n[1] Sim / [2] Não: ")

         if confirmacao == "1":
             novos_aparelhos = []

             for linha in aparelhos:
                if not linha:
                    continue
                if linha[0] != linha_deletar[0]:
                    novos_aparelhos.append(linha)

             with open("data/aparelhos.csv", "w", newline="", encoding="utf-8") as arquivo:
                 escritor = csv.writer(arquivo)
                 escritor.writerow(cabecalho)
                 escritor.writerows(novos_aparelhos)

             print("\nAparelho deletado com sucesso!")

    except FileNotFoundError:
        print("Arquivo de aparelhos não encontrado.")

def atualizar_aparelho():
    execucao=0

    nome_aparelho=input("Digite o nome do aparelho: ").strip()

    with open("data/aparelhos.csv", 'r', newline='', encoding='utf-8') as arquivo, \
        open("data/aparelhos_temp.csv", 'w', newline='', encoding='utf-8') as arquivo_temp:
        leitor = csv.reader(arquivo)
        cabecalho = next(leitor)
        aparelhos = list(leitor)

        aparelhos_encontrados = []
        posicoes = []

        posicao_atual = 0

        for linha in aparelhos:
            if not linha:
                continue
            if linha[1].strip().lower() == nome_aparelho.lower():
                aparelhos_encontrados.append(linha)
                posicoes.append(posicao_atual)
            posicao_atual = posicao_atual + 1

        if len(aparelhos_encontrados) == 0:
            print("Aparelho não encontrado!")
            return
        if len(aparelhos_encontrados) > 1:
            print(f"\nForam encontrados {len(aparelhos_encontrados)} aparelhos com esse nome:\n")

            numero = 1 
            
            for linha in aparelhos_encontrados:
                print(f" [{numero}] ID: {linha[0]} > Setor: {linha[2]} > Tensão: {linha[4]}V")
                numero = numero + 1
            while True:
                escolha_numero = input("\n▸ Digite o número do aparelho que deseja editar: ")
                if escolha_numero.isdigit() and 1 <= int(escolha_numero) <= len(aparelhos_encontrados):
                    posicao_escolhida = posicoes[int(escolha_numero) - 1]
                    break
                else:
                    print("Opção inválida. Tente novamente.")
        else:
            posicao_escolhida = posicoes[0]

    i = aparelhos[posicao_escolhida]

    while True:
        print(f"1- Nome:          {i[1]}\n2- Setor:         {i[2]}\n3- Tensão:        {i[4]}\n4- ID do Sensor:  {i[3]}\n5- Amperagem:     {i[5]}\n6- Horas:         {i[6]}")
        escolha=int(input("Escolha um para editar: \n"))
        if escolha==1:
            print(f"Setor atual: {i[1]}")
            nome=input("\nDigite o novo nome do aparelho: ").strip()
            execucao = 2
            i[1] = nome.strip()
        elif escolha==2:
            print(f"Setor atual: {i[2]}")
            setor_aparelho=input("\nDigite o novo setor do aparelho: ")
            execucao=2
            i[2] = setor_aparelho.strip()
        elif escolha==3:
            print(f"Voltagem atual: {i[4]}")
            voltagem_aparelho=input("\nDigite a nova voltagem do aparelho: ")
            execucao=2
            i[4] = voltagem_aparelho.strip()
        elif escolha==4:
            print(f"ID do sensor atual atual: {i[3]}")
            id_sensor=input("\nDigite o novo ID do Sensor: ")
            execucao=2
            i[3] = id_sensor.strip()
        elif escolha==5:
            print(f"Amperagem atual: {i[5]}")
            amperagem_aparelho=input("\nDigite a nova amperagem do aparelho: ")
            execucao=2
            i[5] = amperagem_aparelho.strip()
        elif escolha==6:
            print(f"Horas atuais: {i[6]}")
            horas=input("\nDigite a nova quantidade de horas do aparelho: ")
            execucao=2
            i[6] = horas.strip()
        else:
            print("\nOpção inválida")
            continue

        while True:
            escolha=int(input("\nVocê deseja editar mais alguma informação? [1] Sim \ [2] Não: "))
            if escolha == 1:
                break
            elif escolha == 2:
                execucao_loop = False
                break 
            else:
                print("Opção inválida! Digite 1 ou 2.")
        if not execucao_loop:
            break
        
        aparelhos[posicao_escolhida] = i 

        with open("data/aparelhos_temp.csv", "w", newline="", encoding="utf-8") as arquivo_temp:
            escritor = csv.writer(arquivo_temp)
            escritor.writerow(cabecalho)
            escritor.writerows(aparelhos)

        if execucao==2:
            os.replace("data/aparelhos_temp.csv", "data/aparelhos.csv")
            print("Aparelho atualizado")

def analisar_aparelho():
    nome_aparelho_analisar = input("\nDigite o nome do aparelho que você deseja analisar: ").strip()

    aparelhos_encontrados = []

    with open("data/aparelhos.csv", "r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        cabecalho = next(leitor)

        for linha in leitor:
            if not linha:
                continue
            if linha[1].strip().lower() == nome_aparelho_analisar.strip().lower():
                aparelhos_encontrados.append(linha)

    if len(aparelhos_encontrados) == 0:
        print("\nAparelho não encontrado no cadastro.")
        return
        
    print(f"\nEncontramos {len(aparelhos_encontrados)} aparelho(s) com esse nome:")

    for i in aparelhos_encontrados:
        print(f"\nId do Equipamento: {i[0]}")
        print(f"Nome: {i[1].capitalize()}")
        print(f"Setor: {i[2].capitalize()}")
        print(f"Id do Sensor: {i[3]}")
        print(f"Tensão Prevista: {i[4]}V")
        print(f"Corrente Prevista: {i[5]}A")
        print(f"Horas Previstas: {i[6]}h")

    dados_aparelhos_escolhidos = []

    if len(aparelhos_encontrados) == 1:
        dados_aparelhos_escolhidos = aparelhos_encontrados[0]
        
    if len(aparelhos_encontrados) > 1: 
        id_valido = 0
        while id_valido == 0:
            id_escolhido = input("\nDigite o ID do equipamento que deseja analisar: ").strip()

            for i in aparelhos_encontrados:
                if i[0] == id_escolhido:
                    dados_aparelhos_escolhidos = i 
                    id_valido = 1
            if id_valido == 0:
                print("ID do equipamento inválido! Tente novamente.")

    print("\nAparelho selecionado com sucesso!")

    id_sensor = dados_aparelhos_escolhidos[3]
    tensao_prevista = float(dados_aparelhos_escolhidos[4])
    corrente_prevista = float(dados_aparelhos_escolhidos[5])
    horas_prevista = float(dados_aparelhos_escolhidos[6])

    print(f"\nCOMPARAÇÃO COM HISTÓRICO DO ARDUINO (ID Sensor: {id_sensor})\n")

    dados_arduino_aparelho = 0

    with open("data/dados_arduino.csv", 'r', newline='', encoding='utf-8') as arquivo_arduino:
        leitor_arduino = csv.reader(arquivo_arduino)
        cabecalho_arduino = next(leitor_arduino)

        for linha in leitor_arduino:
            if not linha:
                continue
            if linha[1].strip().lower() == id_sensor.strip().lower():
                dados_arduino_aparelho = 1

                timestamp = linha[0]
                tensao_real = float(linha[2])
                corrente_real = float(linha[3])
                horas_real = float(linha[4])

                print(f"Medição em: {timestamp}")
                print(f" --> Tensão: Real {tensao_real}V vs Prevista {tensao_prevista}V")
                print(f" --> Corrente: Real {corrente_real}A vs Prevista {corrente_prevista}A")
                print(f" --> Horas: Real {horas_real}h vs Prevista {horas_prevista}h")

                limite_tensao = tensao_prevista * 1.40
                if tensao_real >= limite_tensao:
                    print(f"\nAlerta: A tensão {tensao_real}V é 40% ou mais maior que o previsto ({tensao_prevista}V)! Investigue o equipamento.")
    
                limite_corrente = corrente_prevista * 1.40
                if corrente_real >= limite_corrente:
                    print(f"\nAlerta: A corrente {corrente_real}A é 40% ou mais maior que o previsto ({corrente_prevista}A)! Investigue o equipamento.")

                limite_horas = horas_prevista * 1.40
                if horas_real >= limite_horas:
                    print(f"\nAlerta: O horário {horas_real}h é 40% ou mais maior que o previsto ({horas_prevista}h)! Investigue o equipamento.")


    if dados_arduino_aparelho == 0:
        print("Aviso: Nenhum dado real foi enviado por este sensor ainda.")

