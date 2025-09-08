import socket

IP_MONITOR = ''
PORT = 9300

def run_monitor():
    try:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.bind((IP_MONITOR, PORT))
        srv.listen(5)
        print(f"[MONITOR] Esperando notificaciones en {IP_MONITOR}:{PORT}...")
    except Exception as e:
        print(f"[MONITOR] Error al iniciar el servidor: {e}")
        return

    while True:
        try:
            conn, addr = srv.accept()
            try:
                mensaje = conn.recv(1024).decode()
                print(f"[MONITOR] Notificación desde [{addr}]: {mensaje}")
            except Exception as e:
                print(f"[MONITOR] Error al recibir datos: {e}")
            finally:
                conn.close()
        except Exception as e:
            print(f"[MONITOR] Error al aceptar conexión: {e}")

if __name__ == "__main__":
    run_monitor()