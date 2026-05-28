import csv

def kwh_para_reais ():

    amperagem = int(input("\nAmperagem: ")) # depois mudar todas essas variáveis para float
    voltagem = int(input("Voltagem: "))
    horas_uso = int(input("Horas de uso: "))
    TARIFA_BASE = 0.77
    bandeira_tarifaria = input("Bandeira tarifária atual: ").lower().strip()
    PIS_COFINS = 0.05 # valor que oscila todo mês, pensar em um jeito depois para ele ir mudando
    ICMS = 0.205

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


def deletar_aparelho():
    nome_aparelho_deletar = input("\nDigite o nome do aparelho que você deseja deletar: ")

    try:
         with open ("data/aparelhos.csv", "r", newline="", encoding="utf-8") as arquivo:
            leitor = csv.reader(arquivo)
            aparelhos = list(leitor)

         novos_aparelhos = []

         for linha in aparelhos:
            if not linha:
                continue 
            if linha[0].lower() == nome_aparelho_deletar.lower():
                print(f"\nAparelho encontrado!\nNome: {linha[0]} - Setor: {linha[1]} - Voltagem: {linha[2]}")
                confirmacao = input("Tem certeza que deseja deletar esse aparelho? [1] Sim / [2] Não: ")

                if confirmacao == "1":
                    print("Aparelho deletado com sucesso!")

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

            
 


    
