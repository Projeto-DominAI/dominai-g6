import csv
from src import funcoes
import src.menus as ui
import os

os.system("cls")
escolha = int(input(ui.MENU_PRINCIPAL))

os.system("cls")

if escolha == 1:
    print(ui.TITULO_CADASTRAR)
    funcoes.cadastrar_aparelho()
    os.system("cls")

if escolha == 2:
    print(ui.TITULO_VISUALIZAR)
    funcoes.visualizar_aparelhos()

if escolha == 3:
    print(ui.TITULO_EDITAR)
    funcoes.atualizar_aparelho()

if escolha == 4:
    print(ui.TITULO_DELETAR)
    funcoes.deletar_aparelho()

if escolha == 10:
    funcoes.calcular()
    