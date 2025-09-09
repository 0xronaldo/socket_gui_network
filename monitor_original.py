import socket 


IP = "192.168.100.x"   # IP del monitor 
PORT = 9300              # Puerto que escucha 

def run_monitor(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((IP, PORT)) 
    s.listen(5) 
    print(f"[MONITOR] Esperando notificaciones en {PORT}...") 

    while True: 
        conn, addr = s.accept() 
        msg = conn.recv(1024).decode() 
        print(f"[MONITOR] Notificación recibida: {msg}") 
        conn.close() 

if __name__ == "__main__": 
    run_monitor()