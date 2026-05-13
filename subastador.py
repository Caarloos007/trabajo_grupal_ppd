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

# Registro de respuestas en la ronda actual
respuestas_ronda = {}  # {cliente_addr: "PUJA" o "PASO"}
clientes_paso = 0


def broadcast(msg):
    with lock:
        for c in clientes[:]:
            try:
                c.sendall(msg.encode())
            except:
                clientes.remove(c)


def manejar_cliente(conn, addr):
    global mejor_puja, mejor_cliente, subasta_activa, clientes_paso, respuestas_ronda

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

            if data == "PASO":
                if not subasta_activa:
                    conn.sendall("No hay subasta activa".encode())
                    continue
                
                with lock:
                    if addr not in respuestas_ronda:
                        respuestas_ronda[addr] = "PASO"
                        clientes_paso += 1
                
                broadcast(f"{addr} ha pasado")
                print(f"{addr} ha pasado")

            elif data.startswith("PUJA:"):
                if not subasta_activa:
                    conn.sendall("No hay subasta activa".encode())
                    continue

                try:
                    valor = int(data.split(":")[1])

                    if valor >= mejor_puja + 10:
                        mejor_puja = valor
                        mejor_cliente = addr
                        
                        with lock:
                            if addr in respuestas_ronda:
                                if respuestas_ronda[addr] == "PASO":
                                    clientes_paso -= 1
                            respuestas_ronda[addr] = "PUJA"

                        broadcast(f"NUEVA MEJOR PUJA: ${mejor_puja} por {addr}")
                    else:
                        conn.sendall(f"Puja muy baja. Debe ser +10 sobre {mejor_puja}".encode())

                except:
                    conn.sendall("Error en la puja".encode())

        except:
            break

    with lock:
        if conn in clientes:
            clientes.remove(conn)
        if addr in respuestas_ronda:
            if respuestas_ronda[addr] == "PASO":
                clientes_paso -= 1
            del respuestas_ronda[addr]

    conn.close()


def esperar_pujas():
    global subasta_activa, mejor_puja, mejor_cliente, producto_actual, respuestas_ronda, clientes_paso
    
    respuestas_ronda.clear()
    clientes_paso = 0
    
    print(f"\nRonda abierta. Clientes conectados: {len(clientes)}")
    print("Esperando respuestas de los clientes...")
    print("(Presiona Enter para terminar la ronda)")
    
    # Thread para leer Enter del administrador
    def leer_enter():
        global subasta_activa
        input()  # Espera a que presione Enter
        subasta_activa = False
        print("Ronda terminada por administrador")
    
    thread_enter = threading.Thread(target=leer_enter, daemon=True)
    thread_enter.start()
    
    # Esperar a que termine la ronda (admin presiona enter o se cumpla la condición automática)
    while subasta_activa:
        time.sleep(0.5)
    
    # La puja ha terminado
    if mejor_cliente:
        mensaje = f"SUBASTA TERMINADA. Ganador {mejor_cliente} con ${mejor_puja}"
        broadcast(mensaje)
        print(f"\n{mensaje}")
    else:
        broadcast("Subasta terminada sin pujas")
        print("\nSubasta terminada sin pujas")


def iniciar_subasta():
    global subasta_activa, producto_actual, mejor_puja, mejor_cliente

    print("\n--- CONFIGURAR SUBASTA ---")
    producto_actual = input("Nombre del producto: ")
    mejor_puja = int(input("Precio mínimo: "))
    mejor_cliente = None

    subasta_activa = False

    print(f"\nProducto configurado: {producto_actual} | Precio mínimo: ${mejor_puja}")
    print(f"Clientes conectados actualmente: {len(clientes)}")
    
    # Permitir que el subastador inicie la subasta manualmente
    while True:
        cmd = input("\n¿Listo para iniciar la subasta? (escribe 'iniciar' o 'cancelar'): ").lower().strip()
        
        if cmd == "iniciar":
            if len(clientes) == 0:
                print("Advertencia: No hay clientes conectados")
                confirm = input("¿Continuar de todas formas? (s/n): ").lower().strip()
                if confirm != "s":
                    continue
            
            subasta_activa = True
            broadcast(f"SUBASTA INICIADA: {producto_actual} | Precio mínimo: ${mejor_puja}")
            print(f"Subasta iniciada: {producto_actual}")
            print("Presiona Enter para terminar la ronda")
            break
        elif cmd == "cancelar":
            print("Subasta cancelada")
            return
        else:
            print("Por favor, escribe 'iniciar' o 'cancelar'")
    
    # Esperar a que terminen las pujas (o que admin presione Enter)
    esperar_pujas()
    
    # Después de la ronda, mostrar el menú
    while True:
        cmd = input("\n¿Otro artículo (nuevo) o cerrar? Escribe 'nuevo' o 'cerrar': ").lower().strip()

        if cmd == "cerrar":
            broadcast("Subasta cerrada por el administrador")
            print("\nSubasta cerrada")
            break
        elif cmd == "nuevo":
            broadcast("Reiniciando subasta...")
            print("\nPróximo artículo...")
            iniciar_subasta()
            break
        else:
            print("Por favor, escribe 'nuevo' o 'cerrar'")


def servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Servidor activo en {HOST}:{PORT}")

        # Thread para iniciar subasta
        threading.Thread(target=iniciar_subasta, daemon=True).start()

        while True:
            conn, addr = s.accept()
            with lock:
                clientes.append(conn)

            print(f"Cliente conectado: {addr} (Total: {len(clientes)})")

            threading.Thread(
                target=manejar_cliente,
                args=(conn, addr),
                daemon=True
            ).start()


if __name__ == "__main__":
    servidor()


def iniciar_subasta():
    global subasta_activa, producto_actual, mejor_puja, mejor_cliente

    print("\n--- CONFIGURAR SUBASTA ---")
    producto_actual = input("Nombre del producto: ")
    mejor_puja = int(input("Precio mínimo: "))
    mejor_cliente = None

    subasta_activa = False

    print(f"\nProducto configurado: {producto_actual} | Precio mínimo: ${mejor_puja}")
    print(f"Clientes conectados actualmente: {len(clientes)}")
    
    # Permitir que el subastador inicie la subasta manualmente
    while True:
        cmd = input("\n¿Listo para iniciar la subasta? (escribe 'iniciar' o 'cancelar'): ").lower().strip()
        
        if cmd == "iniciar":
            if len(clientes) == 0:
                print("Advertencia: No hay clientes conectados")
                confirm = input("¿Continuar de todas formas? (s/n): ").lower().strip()
                if confirm != "s":
                    continue
            
            subasta_activa = True
            broadcast(f"SUBASTA INICIADA: {producto_actual} | Precio mínimo: ${mejor_puja}")
            print(f"Subasta iniciada: {producto_actual}")
            break
        elif cmd == "cancelar":
            print("Subasta cancelada")
            return
        else:
            print("Por favor, escribe 'iniciar' o 'cancelar'")
    
    # Esperar a que terminen los 10 segundos
    esperar_pujas()
    
    # Después del timeout, mostrar el menú
    while True:
        cmd = input("\n¿Otro artículo (nuevo) o cerrar? Escribe 'nuevo' o 'cerrar': ").lower().strip()

        if cmd == "cerrar":
            broadcast("Subasta cerrada por el administrador")
            print("\nSubasta cerrada")
            break
        elif cmd == "nuevo":
            broadcast("Reiniciando subasta...")
            print("\nPróximo artículo...")
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