import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 65432

clientes = []
lock = threading.Lock()

subasta_activa = False
producto_actual = ""
mejor_puja = 0
mejor_cliente = None
tiempo_timeout = 10  # 10 segundos para pujar
tiempo_conexion = 25  # 25 segundos para conectarse


def broadcast(msg):
    with lock:
        for c in clientes[:]:
            try:
                c.sendall(msg.encode())
            except:
                clientes.remove(c)


def manejar_cliente(conn, addr):
    global mejor_puja, mejor_cliente, subasta_activa

    print(f"[NUEVO CLIENTE] {addr}")

    while True:
        try:
            # Usar timeout para no bloquear indefinidamente
            conn.settimeout(1)
            try:
                data = conn.recv(1024).decode().strip()
            except socket.timeout:
                continue
            
            if not data:
                break

            if data.startswith("PUJA:"):
                if not subasta_activa:
                    conn.sendall("No hay subasta activa".encode())
                    continue

                try:
                    valor = int(data.split(":")[1])

                    if valor >= mejor_puja + 10:
                        mejor_puja = valor
                        mejor_cliente = addr

                        broadcast(f"🔥 NUEVA MEJOR PUJA: ${mejor_puja} por {addr}")
                    else:
                        conn.sendall(f"❌ Puja muy baja. Debe ser +10 sobre {mejor_puja}".encode())

                except:
                    conn.sendall("Error en la puja".encode())

        except:
            break

    with lock:
        if conn in clientes:
            clientes.remove(conn)

    conn.close()


def esperar_pujas():
    global subasta_activa, mejor_puja, mejor_cliente, producto_actual
    
    print(f"\n⏲ Esperando 25 segundos para que se conecten los clientes...")
    time.sleep(tiempo_conexion)
    
    print(f"\n📢 Comenzando recepción de pujas por 10 segundos...")
    time.sleep(tiempo_timeout)
    
    # La puja ha terminado
    subasta_activa = False
    
    if mejor_cliente:
        mensaje = f"🏆 SUBASTA TERMINADA. Ganador {mejor_cliente} con ${mejor_puja}"
        broadcast(mensaje)
        print(f"\n{mensaje}")
    else:
        broadcast("🏁 Subasta terminada sin pujas")
        print("\n🏁 Subasta terminada sin pujas")


def iniciar_subasta():
    global subasta_activa, producto_actual, mejor_puja, mejor_cliente

    print("\n--- CONFIGURAR SUBASTA ---")
    producto_actual = input("Nombre del producto: ")
    mejor_puja = int(input("Precio mínimo: "))
    mejor_cliente = None

    subasta_activa = True

    broadcast(f"🚀 SUBASTA INICIADA: {producto_actual} | Precio mínimo: ${mejor_puja}")
    print(f"🚀 Subasta iniciada: {producto_actual}")

    # Esperar a que terminen los 10 segundos
    esperar_pujas()
    
    # Después del timeout, mostrar el menú
    while True:
        cmd = input("\n¿Otro artículo (nuevo) o cerrar? Escribe 'nuevo' o 'cerrar': ").lower().strip()

        if cmd == "cerrar":
            broadcast("📴 Subasta cerrada por el administrador")
            print("\n📴 Subasta cerrada")
            break
        elif cmd == "nuevo":
            broadcast("🔄 Reiniciando subasta...")
            print("\n🔄 Próximo artículo...")
            iniciar_subasta()
            break
        else:
            print("Por favor, escribe 'nuevo' o 'cerrar'")


def servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Servidor activo en {HOST}:{PORT}")

        threading.Thread(target=iniciar_subasta, daemon=True).start()

        while True:
            conn, addr = s.accept()
            with lock:
                clientes.append(conn)

            threading.Thread(
                target=manejar_cliente,
                args=(conn, addr),
                daemon=True
            ).start()


if __name__ == "__main__":
    servidor()