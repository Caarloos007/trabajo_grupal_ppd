import socket
import threading

HOST = "127.0.0.1"
PORT = 65432

puja_en_curso = False
esperando_mostrado = False
paso_enviado = False
paso_mostrado = False


def escuchar(sock):
    global puja_en_curso, esperando_mostrado, paso_enviado, paso_mostrado
    
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(f"\n📢 {msg}")
            
            if "🚀 SUBASTA INICIADA" in msg:
                puja_en_curso = True
                esperando_mostrado = False
                paso_enviado = False
                paso_mostrado = False
            elif "🏆 SUBASTA TERMINADA" in msg or "🏁 Subasta terminada" in msg:
                puja_en_curso = False
                if not esperando_mostrado:
                    print("\n⏳ Esperando próxima subasta...")
                    esperando_mostrado = True
                paso_enviado = False
                paso_mostrado = False
            elif "🔄 Reiniciando subasta" in msg:
                puja_en_curso = True
                esperando_mostrado = False
                paso_enviado = False
                paso_mostrado = False
        except:
            break


def cliente():
    global puja_en_curso, esperando_mostrado, paso_enviado, paso_mostrado
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Conectado a la subasta")

            threading.Thread(target=escuchar, args=(s,), daemon=True).start()

            while True:
                if puja_en_curso:
                    esperando_mostrado = False
                    if paso_enviado:
                        if not paso_mostrado:
                            print("\n⏳ Has pasado. Esperando que termine la subasta...")
                            paso_mostrado = True
                        threading.Event().wait(1)
                        continue

                    entrada = input("\n💰 Puja (número) o 'paso': ").strip().lower()

                    if entrada == "paso":
                        s.sendall("PASO".encode())
                        paso_enviado = True
                    elif entrada.isdigit():
                        mensaje = f"PUJA:{entrada}"
                        s.sendall(mensaje.encode())
                    elif entrada:
                        print("❌ Introduce un número o 'paso'")
                else:
                    if not esperando_mostrado:
                        print("\n⏳ Esperando próxima subasta...")
                        esperando_mostrado = True
                    threading.Event().wait(0.5)

        except ConnectionRefusedError:
            print("Servidor no disponible")


if __name__ == "__main__":
    cliente()