import socket, json
import tkinter as tk
from datetime import datetime

SERVER_IP = "192.168.100.37"
SERVER_PORT = 9200
NOTIFY_IP = "192.168.100.52"
NOTIFY_PORT = 9300
LOG_FILE = "srv_log.txt"

def log_message(msg, msg_box):
    regtiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{regtiempo} - {msg}\n"
    msg_box.insert(tk.END, line)
    msg_box.see(tk.END)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

methods = {
    "echo": lambda msg: f"[SERVIDOR] recibio: {msg}"
}

def notify_other_team(msg_box):
    try:
        sock = socket.create_connection((NOTIFY_IP, NOTIFY_PORT), timeout=5)
        sock.sendall("[SERVER] escucha, establecio conexion".encode())
        sock.close()
        log_message("[SERVER] Notificacion enviada al monitor", msg_box)
    except Exception as e:
        log_message(f"[SERVER] No se pudo notificar: {e}", msg_box)

def check_connections(s, msg_box, root):
    try:
        conn, addr = s.accept()
        log_message(f"[SERVER] Cliente conectado: {addr}", msg_box)

        notify_other_team(msg_box)

        data = conn.recv(1024).decode()
        if data:
            request = json.loads(data)
            method = request.get("method")
            params = request.get("params", [])
            result = methods.get(method, lambda *a: "Método no encontrado")(*params)

            response = json.dumps({"result": result}).encode()
            conn.sendall(response)

        conn.close()
    except BlockingIOError:
        pass
    root.after(500, check_connections, s, msg_box, root)

def start_server(msg_box, root):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER_IP, SERVER_PORT))
    s.listen(5)
    s.setblocking(False)
    log_message(f"[SERVER] Escuchando en {SERVER_IP}:{SERVER_PORT}", msg_box)
    root.after(500, check_connections, s, msg_box, root)

# Interfaz
root = tk.Tk()
root.title("Servidor RPC")
msg_box = tk.Text(root, width=60, height=20)
msg_box.pack()

btn = tk.Button(root, text="Iniciar Servidor", command=lambda: start_server(msg_box, root))
btn.pack()

root.mainloop()
