import socket, json

SERVER_IP = "192.168.100.x"   # Cambiar según tu red
SERVER_PORT = 9200

def rpc_call(method, params):
    try:
        s = socket.create_connection((SERVER_IP, SERVER_PORT), timeout=5)
        req = {"method": method, "params": params}
        s.sendall(json.dumps(req).encode())

        resp = json.loads(s.recv(1024).decode())
        s.close()
        return resp.get("result", "Respuesta inválida")
    except Exception as e:
        return f"[CLIENT] Error en llamada RPC: {e}"

if __name__ == "__main__":
    print("[CLIENT] Enviando mensaje RPC...")
    resultado = rpc_call("echo", ["Hola servidor RPC"])
    print(f"[CLIENT] Respuesta: {resultado}")
