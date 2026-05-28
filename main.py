import csv
import src.functions as functions
import src.menus as ui
import os

os.system("cls")

escolha = int(input(ui.MENU_PRINCIPAL))

if escolha == 1:
    os.system("cls")
    print(ui.TITULO_CADASTRAR)
    functions.cadastrar_aparelho()

if escolha == 2:
    functions.visualizar_aparelhos()

if escolha == 10:
    functions.kwh_para_reais()
    