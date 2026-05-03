import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 65432

puja_en_curso = True
tiempo_espera = 0


def escuchar(sock):
    global puja_en_curso, tiempo_espera
    
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(f"\n📢 {msg}")
            
            if "🚀 SUBASTA INICIADA" in msg:
                puja_en_curso = True
                tiempo_espera = 10
            elif "🏆 SUBASTA TERMINADA" in msg or "🏁 Subasta terminada" in msg:
                puja_en_curso = False
                tiempo_espera = 0
            elif "🔄 Reiniciando subasta" in msg:
                puja_en_curso = True
                tiempo_espera = 10
        except:
            break


def cliente():
    global puja_en_curso, tiempo_espera
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Conectado a la subasta")

            threading.Thread(target=escuchar, args=(s,), daemon=True).start()

            while True:
                if puja_en_curso:
                    print(f"\n⏰ Tienes 10 segundos para pujar (escribe tu puja o Enter para pasar):")
                    entrada = input()

                    if entrada.lower() == "salir":
                        break

                    if entrada and entrada.isdigit():
                        mensaje = f"PUJA:{entrada}"
                        s.sendall(mensaje.encode())
                    elif entrada:
                        print("Introduce un número válido")
                else:
                    print("\nEsperando próxima subasta...")
                    time.sleep(1)

        except ConnectionRefusedError:
            print("Servidor no disponible")


if __name__ == "__main__":
    cliente()