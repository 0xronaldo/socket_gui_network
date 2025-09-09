import socket, json 

 

# IPs y puertos 
SERVER_IP = "192.168.100.x"    # Servidor principal (donde está este código) 
SERVER_PORT = 9200               # Puerto para clientes RPC 
NOTIFY_IP = "192.168.100.x"    # Otro equipo en la red al que notificaremos 
NOTIFY_PORT = 9300               # Puerto del "equipo monitor" 

 

# RPC simple 
def echo(msg): 
    return f"Servidor recibió: {msg}" 

 

methods = { 
    "echo": echo 
} 

 

def notify_other_team(): 
    """Envía un mensaje automático a otro equipo en la red.""" 
    try: 
        sock = socket.create_connection((NOTIFY_IP, NOTIFY_PORT)) 
        sock.sendall(b"[SERVER] Estoy en escucha y recibí conexión") 
        sock.close() 
    except Exception as e: 
        print(f"[SERVER] No se pudo notificar al otro equipo: {e}") 

 

def run_server(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((SERVER_IP, SERVER_PORT)) 
    s.listen(5) 
    print(f"[SERVER] Esperando clientes en {SERVER_PORT}...") 

 

    while True: 
        conn, addr = s.accept() 
        print(f"[SERVER] Cliente conectado: {addr}") 

        # Al conectarse un cliente, notificamos a otro equipo 
        notify_other_team() 

        # Recibir datos del cliente 
        data = conn.recv(1024).decode() 
        if not data: 
            conn.close() 
            continue 

 

        # Procesar RPC 
        request = json.loads(data) 
        method = request.get("method") 
        params = request.get("params", []) 

 

        if method in methods: 
            result = methods[method](*params) 
        else: 
            result = "Método no encontrado" 
            response = json.dumps({"result": result}).encode() 
        
        conn.sendall(response) 
        conn.close() 

if __name__ == "__main__": 
    run_server()