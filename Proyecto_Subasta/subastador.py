import socket
import threading
import time

# Configuración del servidor
HOST = '127.0.0.1'  # IP local
PORT = 65432        # Puerto de escucha

# Lista para guardar a los compradores (suscriptores)
suscriptores = []

def enviar_a_todos(mensaje):
    #Nodo emisor de eventos que envía datos a los suscriptores
    for cliente in suscriptores:
        try:
            cliente.sendall(mensaje.encode('utf-8'))
        except:
            suscriptores.remove(cliente)

def logica_subasta():
    #Mensajes y datos dinámicos (cambios en tiempo real)
    print("[LOG] Esperando 10 segundos a que se unan los compradores...")
    time.sleep(10)
    
    producto = "Laptop Gamer Pro"
    precio = 500
    
    while precio <= 1000:
        aviso = f"SUBASTA ACTIVA: {producto} | Puja actual: ${precio}"
        print(f"[LOG EMISOR] Difundiendo: {aviso}")
        enviar_a_todos(aviso)
        precio += 100  # El precio cambia en tiempo real
        time.sleep(4)  # Pausa entre actualizaciones
    
    enviar_a_todos("¡SUBASTA FINALIZADA! Gracias por participar.")
    print("[LOG] Fin de la subasta.")

def iniciar_servidor():
    #Uso de Sockets para aplicación distribuida
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"--- SERVIDOR INICIADO EN {HOST}:{PORT} ---")
        
        # Hilo para que la subasta corra mientras el servidor acepta más gente
        threading.Thread(target=logica_subasta, daemon=True).start()
        
        while True:
            conn, addr = s.accept()
            suscriptores.append(conn)
            print(f"[LOG] Nuevo suscriptor conectado desde {addr}")

if __name__ == "__main__":
    iniciar_servidor()