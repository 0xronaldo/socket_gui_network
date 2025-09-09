import socket, json

# Configuración del servidor
SERVER_IP = "192.168.100.x"   # Cambiar según tu red
SERVER_PORT = 9200              # Puerto para clientes RPC
NOTIFY_IP = "192.168.100.x"   # IP del equipo monitor
NOTIFY_PORT = 9300              # Puerto del monitor

# Métodos RPC
def echo(msg):
    return f"Servidor recibió: {msg}"

methods = {
    "echo": echo
}

def notify_other_team():
    """Envía un mensaje automático al monitor."""
    try:
        sock = socket.create_connection((NOTIFY_IP, NOTIFY_PORT), timeout=5)
        sock.sendall("[SERVER] en escucha, establecio conexión".encode("utf-8"))
        sock.close()
        print("[SERVER] Notificación enviada al monitor.")
    except Exception as e:
        print(f"[SERVER] No se pudo notificar al monitor: {e}")

def run_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen(5)
        print(f"[SERVER] Esperando clientes en {SERVER_IP}:{SERVER_PORT}...")
    except Exception as e:
        print(f"[SERVER] Error iniciando servidor: {e}")
        return

    while True:
        try:
            conn, addr = s.accept()
            print(f"[SERVER] Cliente conectado: {addr}")

            # Avisar al monitor
            notify_other_team()

            # Recibir datos del cliente
            data = conn.recv(1024).decode()
            if not data:
                conn.close()
                continue

            # Procesar RPC
            try:
                request = json.loads(data)
                method = request.get("method")
                params = request.get("params", [])

                if method in methods:
                    result = methods[method](*params)
                else:
                    result = "Método no encontrado"
            except Exception as e:
                result = f"Error procesando RPC: {e}"

            # Respuesta al cliente
            response = json.dumps({"result": result}).encode()
            conn.sendall(response)
            conn.close()
        except Exception as e:
            print(f"[SERVER] Error con cliente: {e}")

if __name__ == "__main__":
    run_server()
