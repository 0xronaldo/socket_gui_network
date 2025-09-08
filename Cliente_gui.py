import socket

import json 
import time

SERVER_IP = 'localhost'
SERVER_PORT = 9200

def rpc_call(method, params=None):
    """Realiza una llamada RPC al servidor."""
    if params is None:
        params = []
        
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)  # Timeout de 10 segundos
            s.connect((SERVER_IP, SERVER_PORT))
            
            # Preparar solicitud
            request = {"method": method, "params": params}
            request_json = json.dumps(request, ensure_ascii=False)
            
            print(f"[CLIENT] Enviando: {request_json}")
            s.sendall(request_json.encode('utf-8'))
            
            # Recibir respuesta
            response_data = s.recv(1024).decode('utf-8')
            response = json.loads(response_data)
            
            return response.get("result", "Sin resultado")
            
    except socket.timeout:
        return "Error: Timeout de conexión"
    except ConnectionRefusedError:
        return "Error: Servidor no disponible"
    except json.JSONDecodeError:
        return "Error: Respuesta inválida del servidor"
    except Exception as e:
        return f"Error: {e}"

def run_client_tests():
    """Ejecuta pruebas del cliente."""
    print("=== CLIENTE RPC - PRUEBAS ===")
    
    # Prueba 1: Echo
    print("\n1. Prueba echo:")
    result = rpc_call("echo", ["Hola servidor RPC"])
    print(f"   Resultado: {result}")
    
    # Prueba 2: Hora del servidor
    print("\n2. Prueba get_time:")
    result = rpc_call("get_time")
    print(f"   Resultado: {result}")
    
    # Prueba 3: Suma
    print("\n3. Prueba add:")
    result = rpc_call("add", [5, 3])
    print(f"   Resultado: {result}")
    
    # Prueba 4: Método inexistente
    print("\n4. Prueba método inexistente:")
    result = rpc_call("metodo_falso", ["test"])
    print(f"   Resultado: {result}")


if __name__ == "__main__":
	run_client_tests()
