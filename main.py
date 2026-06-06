import csv
import os
import src.funcoes as functions
import src.menus as ui
import src.auth as auth

auth.criar_csv_empresas()
os.system("cls")

print(ui.MENU_PRINCIPAL_AUTH)
escolha_auth = input("➜ ").strip()

empresa = None

if escolha_auth == "2":
    empresa = auth.cadastrar_empresa()
elif escolha_auth == "1":
    empresa = auth.login_empresa()

if empresa is None:
    print("Encerrando processo.")
else:
    os.system("cls")
    escolha = int(input(ui.MENU_PRINCIPAL))
    os.system("cls")

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

    if escolha == 10:
        functions.calcular(empresa)
