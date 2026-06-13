import serial
import csv
import datetime
import time
import os
import threading

porta = 'COM3'
baudrate = 9600

def inicio_csv():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists("data/dados_arduino.csv"):
        with open ("data/dados_arduino.csv", "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["timestamp", "id_sensor", "tensao", "corrente", "horas"])

def coleta():
    inicio_csv()

    try:
        arduino = serial.Serial(porta, baudrate, timeout=5)
        time.sleep(2)
        print(f"Conectando ao arduino com a porta {porta}")
    
    except serial.SerialException:
        print(f"Erro!!! Não foi possível conectar com a porta {porta}.")
        print("Analise se o arduino foi plugado corretamente e se a porta é a correta.")
        return

    print("Dados sendo coletados em segundo plano... (Ctrl+C para parar)\n")

    with open ("data/dados_arduino.csv", "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)

        while True:
            try:
                linha = arduino.readline().decode('utf-8').strip()
                
                if not linha:
                    continue

                partes = linha.split(',')

                if len(partes) != 4:
                    print(f"O dado foi ignorado por conta do formato inesperado: {linha}")
                    continue

                id_sensor = partes[0]
                tensao = partes[1]
                corrente = partes[2]
                horas = partes[3]
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                escritor.writerow([timestamp, id_sensor, tensao, corrente, horas])
                arquivo.flush()
                print(f"[{timestamp}] [{id_sensor}] -> [{tensao}]V | [{corrente}]A | [{horas}]h")

            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    thread_arduino = threading.Thread(target=coleta, daemon=True)
    
    thread_arduino.start()
    
    try:
        while True:
            print("O programa principal está rodando e livre para outras tarefas...")
            time.sleep(15) 
            
    except KeyboardInterrupt:
        print("\nPrograma principal e coleta de dados encerrados com sucesso.")
