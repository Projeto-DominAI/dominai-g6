import csv
import os
import src.funcoes as functions
import src.menus as ui
import src.auth as auth

auth.criar_csv_empresas()
os.system('cls' if os.name =='nt' else 'clear')

print(ui.MENU_PRINCIPAL_AUTH)
escolha_auth = input("➜ ").strip()

empresa = None

if escolha_auth == "2":
    os.system('cls' if os.name =='nt' else 'clear')
    print(ui.TITULO_CADASTRAR_EMPRESA)
    empresa = auth.cadastro_das_empresas()
elif escolha_auth == "1":
    empresa = auth.login_empresa()

if empresa is None:
    print("Encerrando processo.")
else:
    os.system('cls' if os.name =='nt' else 'clear')
    escolha_valida = 0
    while escolha_valida == 0:
        try:
            escolha = int(input(ui.MENU_PRINCIPAL))
            escolha_valida = 1
        except ValueError:
            print("Erro: Digite apenas números inteiros. Tente novamente. ")

    os.system('cls' if os.name =='nt' else 'clear')

    if escolha == 1:
        print(ui.TITULO_CADASTRAR)
        functions.cadastrar_aparelho()

    if escolha == 2:
        print(ui.TITULO_VISUALIZAR)
        functions.visualizar_aparelhos()

    if escolha == 3:
        print(ui.TITULO_EDITAR)
        functions.atualizar_aparelho()

    if escolha == 4:
        print(ui.TITULO_DELETAR)
        functions.deletar_aparelho()
    
    if escolha == 5:
        print(ui.TITULO_ANALISAR)
        functions.analisar_aparelho()

    if escolha == 10:
        print(ui.CALCULAR_EMPRESA)
        functions.calcular(empresa)
