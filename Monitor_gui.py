import socket
import json
import time

NOTIFY_IP = 'localhost'
NOTIFY_PORT = 9300



def run_monitor():
    """Ejecuta el monitor que escucha notificaciones."""
    monitor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    monitor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        monitor_socket.bind((NOTIFY_IP, NOTIFY_PORT))
        monitor_socket.listen(5)
        print(f"[MONITOR] Esperando notificaciones en {NOTIFY_IP}:{NOTIFY_PORT}...")
        
        while True:
            conn, addr = monitor_socket.accept()
            try:
                msg = conn.recv(1024).decode('utf-8')
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                print(f"[MONITOR] [{timestamp}] Desde {addr}: {msg}")
            except Exception as e:
                print(f"[MONITOR] Error recibiendo mensaje: {e}")
            finally:
                conn.close()
                
    except KeyboardInterrupt:
        print("\n[MONITOR] Cerrando monitor...")
    except Exception as e:
        print(f"[MONITOR] Error: {e}")
    finally:
        monitor_socket.close()


if __name__ == "__main__":
	run_monitor()