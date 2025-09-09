import socket, json


# DEFINICION DE DE LOS DIRECCIONES DE IP_SERVIDOR Y EL MONITOR O AQUIEN NOTIFICAR
# LA IP PARA EL SERVIDOR SERA LA IP DE LA PORTATIL
SERVER_IP = '192.168.100.37'
SERVER_PORT = 9200
NOTIFY_IP = '192.168.100.67'
NOTIFY_PORT = 9300

def echo(msg): return  f"Servidor recibió: {msg}"

methods = {
    "echo": echo   
}


def notify_other_team():
    """enviar un mensaje automatico al monitor"""
    try:
        sock = socket.create_connection((NOTIFY_IP, NOTIFY_PORT))
        sock.sendall(b"[SERVER] Estoy en escucha y recibi conexion")
        sock.close()
    except Exception as e:
        print(f"[SERVER] No pudo notificar al otro Equipo: {e}")

def run_servidor():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # escuchando en la IP y puerto definidos
    srv.bind((SERVER_IP, SERVER_PORT))
    srv.listen(5) # maximo de 5 conexiones en espera cola
    print(f"[SERVER] Esperando clientes en {SERVER_IP}:{SERVER_PORT}...")
    while True:
        conn, addr = srv.accept()
        print(f"[SERVER] Cliente conectado: {addr}")


        # AI conectarse un cliente, notificamos a otro equipo
        notify_other_team()


        # Recibir datos del cliente
        data = conn.recv(1024).decode('utf-8')
        if not data:
            conn.close()
            continue
        # processar RPC

        request = json.loads(data)
        methodo = request.get("method")
        params = request.get("params", [])
        if methodo in methods:
            result = methods[methodo](*params)
        else: 
            result = "Metdodo no encontrado"

        response = json.dumps{{"result":result}.encode()}
        conn.sendall(respuese)
        conn.close()


if __name__ == "__main__"::
    run_servidor()