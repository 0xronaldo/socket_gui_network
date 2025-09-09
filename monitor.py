import socket

IP = "192.168.100.110"   # Cambiar según tu red
PORT = 9300              # Puerto que escucha

def run_monitor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((IP, PORT))
        s.listen(5)
        print(f"[MONITOR] Esperando notificaciones en {IP}:{PORT}...")
    except Exception as e:
        print(f"[MONITOR] Error iniciando monitor: {e}")
        return

    while True:
        try:
            conn, addr = s.accept()
            msg = conn.recv(1024).decode()
            print(f"[MONITOR] Notificación recibida de {addr}: {msg}")
            conn.close()
        except Exception as e:
            print(f"[MONITOR] Error recibiendo notificación: {e}")

if __name__ == "__main__":
    run_monitor()
