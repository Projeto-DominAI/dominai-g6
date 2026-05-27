import functions

print("\n[1] Cadastrar aparelho\n[2] Visualizar aparelhos\n[3] Editar aparelhos\n[4] Deletar aparelhos")
escolha = int(input("---> Escolha: "))

if escolha == 1:
    functions.cadastrar_aparelho()

if escolha == 2:
    functions.visualizar_aparelhos()

if escolha == 10:
    functions.kwh_para_reais()
    