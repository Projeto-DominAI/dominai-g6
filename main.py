import csv
import src.functions as functions
import src.menus as ui
import os

os.system("cls")
escolha = int(input(ui.MENU_PRINCIPAL))

os.system("cls")

if escolha == 1:
    print(ui.TITULO_CADASTRAR)
    functions.cadastrar_aparelho()
    os.system("cls")

if escolha == 2:
    functions.visualizar_aparelhos()

if escolha == 3:
    functions.atualizar_aparelho()

if escolha == 10:
    functions.calcular()
    