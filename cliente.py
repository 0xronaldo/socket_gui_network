import socket, json

SRV_IP = '192.168.100.37'
SRV_PORT = 9200

def rpc_client(method, params):
    """Cliente RPC que envía una solicitud al servidor y recibe la respuesta."""
    try:
        sock = socket.create_connection((SRV_IP, SRV_PORT))
        request = json.dumps({"method": method, "params": params}).encode()
        sock.sendall(request)
        
        response_data = sock.recv(1024).decode('utf-8')
        response = json.loads(response_data)
        sock.close()
        return response.get("result")



    except Exception as e:
        print(f"[CLIENT] Error: {e}")
        return None

if __name__ == "__main__":
    print(rpc_client("echo", "Comunicacion : conectado..."))
    print("[CLIENT] Enviando mensaje RPC...")
    print(rpc_client("echo", ["HOLA SERVIDOR RPC"]))
    print(rpc_client("echo", ["HOLA SERVIDOR RPC"]))



