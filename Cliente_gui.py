import socket, json
import tkinter as tk
from datetime import datetime

SERVER_IP = "192.168.100.x"
SERVER_PORT = 9200
LOG_FILE = "srv_log.txt"

def log_message(msg, msg_box):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} - {msg}\n"
    msg_box.insert(tk.END, line)
    msg_box.see(tk.END)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

def rpc_call(method, params, msg_box):
    try:
        s = socket.create_connection((SERVER_IP, SERVER_PORT), timeout=5)
        req = {"method": method, "params": params}
        s.sendall(json.dumps(req).encode())
        resp = json.loads(s.recv(1024).decode())
        s.close()
        return resp.get("result", "Respuesta invalida")
    except Exception as e:
        error = f"[CLIENT] Error: {e}"
        log_message(error, msg_box)
        return error

def enviar_rpc(entry, msg_box):
    texto = entry.get()
    result = rpc_call("echo", [texto], msg_box)
    log_message(f"[CLIENT] Respuesta: {result}", msg_box)

# Interfaz
root = tk.Tk()
root.title("Cliente RPC")

entry = tk.Entry(root, width=50)
entry.pack()

msg_box = tk.Text(root, width=60, height=20)
msg_box.pack()

btn = tk.Button(root, text="Enviar RPC", command=lambda: enviar_rpc(entry, msg_box))
btn.pack()

root.mainloop()
