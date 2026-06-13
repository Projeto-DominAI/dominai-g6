import csv
import os

arquivo_empresas = "data/empresas.csv"

def criar_csv_empresas():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(arquivo_empresas):
        with open(arquivo_empresas, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["nome", "senha", "grupo", "regime", "atividade"])

def cadastro_das_empresas():
    print("\n Nome da empresa: ", end="")
    nome = input().strip()

    with open(arquivo_empresas, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            if linha["nome"].lower() == nome.lower():
                print("Está empresa já está cadastrada.")
                return None
    
    senha = input("Crie sua senha: ").strip()
    grupo = input("Grupo da empresa que representa: ").lower().lower()
    regime = input("Regime: ").lower().strip()
    atividade = input("Atividade que faz: ").lower().strip()

    with open(arquivo_empresas, "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([nome, senha, grupo, regime, atividade])

    print("\nEmpresa cadastrada com sucesso!")
    return {"nome": nome, "grupo": grupo, "regime": regime, "atividade": atividade}

def login_empresa():
    nome = input("\nNome da empresa: ").strip()
    senha = input("Senha: ").strip()

    with open(arquivo_empresas, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            if linha["nome"].lower() == nome.lower() and linha["senha"] == senha:
                print(f"\nLhes damos as boas vindas, {linha['nome']}!")
                return {"nome": linha["nome"], "grupo": linha["grupo"], "regime": linha["regime"], "atividade": linha["atividade"]}
    print("Nome ou senha incorretos, tente novamente. Caso ainda não tenha um cadastro, faça um!")
    return None