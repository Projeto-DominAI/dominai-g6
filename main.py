from src import funcoes
from src import menus as ui
import os

os.system("cls")

while True:
    escolha = int(input(ui.MENU_PRINCIPAL))

    if escolha == 1:
        os.system("cls")
        print(ui.TITULO_CADASTRAR)
        funcoes.cadastrar_aparelho()
        os.system("cls")
    elif escolha == 2:
        os.system("cls")
        print(ui.TITULO_VISUALIZAR)
        funcoes.visualizar_aparelhos()
    elif escolha == 3:
        os.system("cls")
        print(ui.TITULO_EDITAR)
        funcoes.atualizar_aparelho()
    elif escolha == 4:
        os.system("cls")
        print(ui.TITULO_DELETAR)
        funcoes.deletar_aparelho()
    elif escolha == 10:
        os.system("cls")
        funcoes.calcular()

    print("\nVocê deseja continuar?\n[1] Sim\n[2] Não")
    encerrar = int(input("---> "))

    if encerrar == 1:
        os.system("cls")
        continue
    elif encerrar == 2:
        os.system("cls")
        print("Programa encerrado!")
        break

    
    