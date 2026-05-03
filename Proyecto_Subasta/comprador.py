import socket
import threading

def escuchar_subasta(sock):
    #Uso de threading para recibir datos sin bloquear la consola
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            #Registro en consola de la actividad (Logs)
            print(f"\n[EVENTO RECIBIDO]: {data.decode('utf-8')}")
            print("Escribe 'puja' para participar o 'salir': ", end="")
        except:
            break

def conectar_comprador():
    host = '127.0.0.1'
    port = 65432
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print("--- CONECTADO AL SISTEMA DE SUBASTAS ---")
            
            # Iniciamos el hilo de escucha
            hilo = threading.Thread(target=escuchar_subasta, args=(s,), daemon=True)
            hilo.start()
            
            while True:
                opcion = input("Escribe 'puja' para participar o 'salir': ")
                if opcion.lower() == 'salir':
                    break
                elif opcion.lower() == 'puja':
                    print("[INFO] Puja registrada localmente.")
        except ConnectionRefusedError:
            print("[ERROR] El subastador no está en línea.")

if __name__ == "__main__":
    conectar_comprador()