import socket, json 

 

SERVER_IP = "192.168.100.x" 
SERVER_PORT = 9200 

 

def rpc_call(method, params): 
    s = socket.create_connection((SERVER_IP, SERVER_PORT)) 
    req = {"method": method, "params": params} 
    s.sendall(json.dumps(req).encode()) 
    resp = json.loads(s.recv(1024).decode()) 
    s.close() 
    return resp["result"] 

 
print("[CLIENT] Enviando mensaje RPC...") 
print(rpc_call("echo", ["Hola servidor RPC"])) 